import numpy as np
from datetime import datetime

class JetXAnalyzer:
    def __init__(self):
        self.history = []
        self.current_streak = 0
        self.last_green = None

    def add_result(self, value):
        """Classifica o resultado e atualiza estatísticas."""
        result = {
            "value": value,
            "time": datetime.now().strftime("%H:%M:%S"),
            "category": self.classify(value)
        }

        self.history.append(result)
        
        # Atualiza sequência de verdes/vermelhos
        if "green" in result["category"]:
            self.current_streak += 1
            self.last_green = result
        else:
            self.current_streak = 0

    def classify(self, value):
        """Define a categoria do multiplicador."""
        if value < 1.5:
            return "red"
        elif 1.5 <= value < 3.0:
            return "green-low"
        elif 3.0 <= value < 5.0:
            return "green-medium"
        elif 5.0 <= value < 10.0:
            return "green-high"
        else:
            return "green-super"

    def get_stats(self):
        """Retorna estatísticas em tempo real."""
        if not self.history:
            return None

        last_10 = self.history[-10:]
        reds = sum(1 for r in last_10 if r["category"] == "red")
        greens = 10 - reds

        return {
            "current": self.history[-1],
            "streak": self.current_streak,
            "last_green": self.last_green,
            "red_percentage": (reds / 10) * 100,
            "green_percentage": (greens / 10) * 100,
            "volatility": np.std([r["value"] for r in last_10]) if len(last_10) >= 2 else 0
        }
