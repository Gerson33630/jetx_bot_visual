# app.py - JetX Bot Elephant Bet
from flask import Flask, render_template
import random
from datetime import datetime
import pytz
from threading import Thread, Lock
import time
import requests

app = Flask(__name__)

# Configurações
PREDICTION_INTERVAL = 5  # segundos
HISTORY_SIZE = 50
TIMEZONE = pytz.timezone('Africa/Maputo')
WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/KGVwLURtceRL0jq53ZC99J?mode=ac_t"

# Sistema de classificação
MULTIPLIER_LEVELS = [
    (1.00, 1.49, "🟥 Vermelho", "vermelho"),
    (1.50, 2.99, "🟩 Verde menor", "verde_menor"),
    (3.00, 4.99, "🟩 Verde maior", "verde_maior"),
    (5.00, 9.99, "🟩 Super verde", "super_verde"),
    (10.00, 19.99, "🟩 Ultimato verde", "ultimato_verde"),
    (20.00, 99.99, "🟩 Mega verde", "mega_verde"),
    (100.00, 9999.99, "🟩 Ultra verde", "ultra_verde"),
    (10000.00, 25000.00, "🟩 Alfa verde", "alfa_verde")
]

PROTECTION_MULTIPLIERS = {
    "vermelho": 1.2,
    "verde_menor": 1.5,
    "verde_maior": 2.0,
    "super_verde": 2.5,
    "ultimato_verde": 3.0,
    "mega_verde": 4.0,
    "ultra_verde": 5.0,
    "alfa_verde": 10.0
}

class JetXBot:
    def __init__(self):
        self.history = []
        self.current = None
        self.last_green = None
        self.streak = 0
        self.lock = Lock()
        self.warning_message = ""
        
    def generate_multiplier(self):
        rand = random.random()        
        if rand < 0.7: return round(random.uniform(1.00, 1.99), 2)
        elif rand < 0.9: return round(random.uniform(2.00, 4.99), 2)
        elif rand < 0.98: return round(random.uniform(5.00, 19.99), 2)
        else: return round(random.uniform(20.00, 25000.00), 2)
    
    def classify(self, value):
        for min_val, max_val, label, css_class in MULTIPLIER_LEVELS:
            if min_val <= value <= max_val:
                return label, css_class
        return "🟥 Desconhecido", "vermelho"
    
    def get_protection_multiplier(self, css_class):
        return PROTECTION_MULTIPLIERS.get(css_class, 1.0)
    
    def update_warning_message(self):
        red_count = sum(1 for item in self.history[-10:] if "Vermelho" in item['category'])
        if red_count >= 8:
            self.warning_message = "⚠️ ATENÇÃO: O bot não está acertando. Repouse um pouco, talvez a casa não esteja pagando. Volte a apostar mais tarde."
        else:
            self.warning_message = ""
    
    def update(self):
        while True:
            value = self.generate_multiplier()
            label, css_class = self.classify(value)
            
            with self.lock:
                self.current = {
                    'value': value,
                    'category': label,
                    'css_class': css_class,
                    'time': datetime.now(TIMEZONE).strftime("%H:%M:%S"),
                    'protection': self.get_protection_multiplier(css_class)
                }
                
                if "Verde" in label:
                    self.last_green = self.current
                    self.streak += 1
                else:
                    self.streak = 0
                
                self.history.append(self.current)
                if len(self.history) > HISTORY_SIZE:
                    self.history.pop(0)
                
                self.update_warning_message()
            
            time.sleep(PREDICTION_INTERVAL)

bot = JetXBot()
Thread(target=bot.update, daemon=True).start()

@app.route('/')
def index():
    with bot.lock:
        return render_template('index.html',
            current=bot.current,
            history=bot.history[::-1],  # Histórico completo ordenado do mais recente
            last_green=bot.last_green,
            streak=bot.streak,
            warning_message=bot.warning_message,
            whatsapp_link=WHATSAPP_GROUP_LINK,
            year=datetime.now().year
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
