# app.py - JetX Bot Elephant Bet (Versão Aperfeiçoada)
from flask import Flask, render_template
import random
from datetime import datetime
import pytz
from threading import Thread, Lock
import time
import requests  # Para futuras integrações

app = Flask(__name__)

# Configurações (organizadas em seções)
# --------------------------------------------------
TEMPORAIS = {
    'PREDICTION_INTERVAL': 5,  # segundos
    'HISTORY_SIZE': 50,
    'TIMEZONE': pytz.timezone('Africa/Maputo')
}

LINKS = {
    'WHATSAPP_GROUP': "https://chat.whatsapp.com/KGVwLURtceRL0jq53ZC99J?mode=ac_t",
    'ELEPHANT_BET': "https://elephantbet.com"  # Novo link adicionado
}

# Sistema de classificação (mais legível)
# --------------------------------------------------
MULTIPLIER_CATEGORIES = [
    {'range': (1.00, 1.49), 'label': "🟥 Vermelho", 'class': "vermelho", 'protection': 1.2},
    {'range': (1.50, 2.99), 'label': "🟩 Verde menor", 'class': "verde_menor", 'protection': 1.5},
    {'range': (3.00, 4.99), 'label': "🟩 Verde maior", 'class': "verde_maior", 'protection': 2.0},
    {'range': (5.00, 9.99), 'label': "🟩 Super verde", 'class': "super_verde", 'protection': 2.5},
    {'range': (10.00, 19.99), 'label': "🟩 Ultimato verde", 'class': "ultimato_verde", 'protection': 3.0},
    {'range': (20.00, 99.99), 'label': "🟩 Mega verde", 'class': "mega_verde", 'protection': 4.0},
    {'range': (100.00, 9999.99), 'label': "🟩 Ultra verde", 'class': "ultra_verde", 'protection': 5.0},
    {'range': (10000.00, 25000.00), 'label': "🟩 Alfa verde", 'class': "alfa_verde", 'protection': 10.0}
]

# Probabilidades ajustáveis (facilita futuras modificações)
PROBABILITIES = {
    'red': 0.7,         # 70%
    'green_low': 0.2,   # 20%
    'green_medium': 0.08, # 8%
    'green_high': 0.02  # 2%
}

class JetXBot:
    def __init__(self):
        self.history = []
        self.current = None
        self.last_green = None
        self.streak = 0
        self.lock = Lock()
        self.warning_message = ""
        self.performance_stats = {  # Novo: estatísticas de desempenho
            'total_predictions': 0,
            'green_count': 0,
            'red_count': 0
        }
        
    def generate_multiplier(self):
        """Gera multiplicadores com distribuição mais precisa"""
        rand = random.random()
        
        if rand < PROBABILITIES['red']:
            return round(random.uniform(1.00, 1.99), 2)
        elif rand < PROBABILITIES['red'] + PROBABILITIES['green_low']:
            return round(random.uniform(2.00, 4.99), 2)
        elif rand < PROBABILITIES['red'] + PROBABILITIES['green_low'] + PROBABILITIES['green_medium']:
            return round(random.uniform(5.00, 19.99), 2)
        else:
            return round(random.uniform(20.00, 25000.00), 2)
    
    def classify(self, value):
        """Classificação otimizada com busca direta"""
        for category in MULTIPLIER_CATEGORIES:
            min_val, max_val = category['range']
            if min_val <= value <= max_val:
                return category['label'], category['class'], category['protection']
        return "🟥 Desconhecido", "vermelho", 1.0
    
    def update_stats(self, is_green):
        """Atualiza estatísticas de desempenho"""
        self.performance_stats['total_predictions'] += 1
        if is_green:
            self.performance_stats['green_count'] += 1
        else:
            self.performance_stats['red_count'] += 1
    
    def calculate_accuracy(self):
        """Calcula taxa de acertos"""
        if self.performance_stats['total_predictions'] == 0:
            return 0
        return (self.performance_stats['green_count'] / self.performance_stats['total_predictions']) * 100
    
    def update_warning_message(self):
        """Sistema de alertas aprimorado"""
        red_count = sum(1 for item in self.history[-10:] if "Vermelho" in item['category'])
        
        if red_count >= 8:
            accuracy = self.calculate_accuracy()
            self.warning_message = (
                f"⚠️ ALERTA: Sequência de {red_count} vermelhos\n"
                f"Taxa de acerto atual: {accuracy:.1f}%\n"
                "Considere ajustar sua estratégia!"
            )
        else:
            self.warning_message = ""
    
    def update(self):
        """Loop principal otimizado"""
        while True:
            value = self.generate_multiplier()
            label, css_class, protection = self.classify(value)
            is_green = "Verde" in label
            
            with self.lock:
                self.current = {
                    'value': value,
                    'category': label,
                    'css_class': css_class,
                    'time': datetime.now(TEMPORAIS['TIMEZONE']).strftime("%H:%M:%S"),
                    'protection': protection,
                    'is_green': is_green  # Novo campo para facilitar verificações
                }
                
                if is_green:
                    self.last_green = self.current
                    self.streak += 1
                else:
                    self.streak = 0
                
                self.history.append(self.current)
                if len(self.history) > TEMPORAIS['HISTORY_SIZE']:
                    self.history.pop(0)
                
                self.update_stats(is_green)
                self.update_warning_message()
            
            time.sleep(TEMPORAIS['PREDICTION_INTERVAL'])

bot = JetXBot()
Thread(target=bot.update, daemon=True).start()

@app.route('/')
def index():
    with bot.lock:
        current_stats = {
            'accuracy': bot.calculate_accuracy(),
            'total_predictions': bot.performance_stats['total_predictions'],
            'green_rate': f"{(bot.performance_stats['green_count']/max(1, bot.performance_stats['total_predictions'])*100):.1f}%"
        }
        
        return render_template('index.html',
            current=bot.current,
            history=bot.history[::-1],
            last_green=bot.last_green,
            streak=bot.streak,
            warning_message=bot.warning_message,
            whatsapp_link=LINKS['WHATSAPP_GROUP'],
            bet_link=LINKS['ELEPHANT_BET'],  # Novo link
            stats=current_stats,  # Novo: estatísticas
            year=datetime.now().year
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
