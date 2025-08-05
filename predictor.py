import numpy as np
from datetime import datetime
from config import Config
import pytz

class JetXPredictor:
    def __init__(self):
        self.history = []
        self.trends = []
        self.last_update = None
        
    def add_result(self, value):
        """Adiciona um novo resultado e atualiza as tendências"""
        classified = self.classify(value)
        self.history.append({
            'value': value,
            'category': classified[1],
            'css_class': classified[2],
            'time': datetime.now(Config.TIMEZONE),
            'protection': self.get_protection(classified[2])
        })
        
        # Mantém o histórico dentro do tamanho configurado
        if len(self.history) > Config.HISTORY_SIZE:
            self.history.pop(0)
            
        # Atualiza análise de tendências
        self._update_trends()
        self.last_update = datetime.now(Config.TIMEZONE)
        
    def classify(self, value):
        """Classifica o multiplicador de acordo com os níveis configurados"""
        for min_val, max_val, label, css_class in Config.MULTIPLIER_LEVELS:
            if min_val <= value <= max_val:
                return (value, label, css_class)
        return (value, "🟥 Desconhecido", "red")
    
    def get_protection(self, css_class):
        """Retorna o multiplicador de proteção baseado na estratégia"""
        return Config.PROTECTION_STRATEGY.get(css_class, 1.0)
    
    def _update_trends(self):
        """Analisa tendências com base no histórico recente"""
        if len(self.history) < 5:  # Mínimo para análise
            self.trends = []
            return
            
        recent = self.history[-Config.TREND_ANALYSIS_WINDOW:]
        greens = sum(1 for r in recent if r['css_class'].startswith('green'))
        reds = len(recent) - greens
        
        # Calcula probabilidades empíricas
        self.trends = {
            'green_probability': greens / len(recent),
            'red_probability': reds / len(recent),
            'streak': self._calculate_streak(),
            'volatility': self._calculate_volatility()
        }
    
    def _calculate_streak(self):
        """Calcula a sequência atual de verdes/vermelhos"""
        if not self.history:
            return 0
            
        current_css = self.history[-1]['css_class']
        streak = 0
        
        for item in reversed(self.history):
            if item['css_class'] == current_css:
                streak += 1
            else:
                break
                
        return streak if streak > 1 else 0
    
    def _calculate_volatility(self):
        """Calcula a volatilidade dos últimos resultados"""
        if len(self.history) < 2:
            return 0
            
        values = [item['value'] for item in self.history[-10:]]
        return np.std(values)
    
    def get_warning(self):
        """Gera avisos com base nas tendências"""
        if not self.trends:
            return ""
            
        if self.trends['red_probability'] > Config.WARNING_THRESHOLD:
            return "⚠️ Alta probabilidade de vermelhos consecutivos. Considere reduzir apostas."
        
        if self.trends['volatility'] > 5.0:
            return "⚠️ Alta volatilidade detectada. O jogo está imprevisível."
            
        if self.trends['streak'] >= 5 and self.history[-1]['css_class'].startswith('green'):
            return "⚠️ Sequência longa de verdes. Possível reversão em breve."
            
        return ""
    
    def get_last_green(self):
        """Retorna o último resultado verde"""
        for item in reversed(self.history):
            if item['css_class'].startswith('green'):
                return item
        return None
    
    def get_stats(self):
        """Retorna estatísticas resumidas"""
        if not self.history:
            return {}
            
        return {
            'current': self.history[-1],
            'last_green': self.get_last_green(),
            'streak': self._calculate_streak(),
            'trends': self.trends,
            'warning': self.get_warning(),
            'history_size': len(self.history)
        }
