import pytz
from datetime import timedelta

class Config:
    # Configurações gerais
    PREDICTION_INTERVAL = timedelta(seconds=15)
    HISTORY_SIZE = 100
    TIMEZONE = pytz.timezone('Africa/Maputo')
    
    # URLs e links
    WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/KGVwLURtceRL0jq53ZC99J"
    JETX_GAME_URL = "https://www.elephant.bet/pt/games/jetx"
    
    # Níveis de multiplicador
    MULTIPLIER_LEVELS = [
        (1.00, 1.49, "🟥 Vermelho", "red"),
        (1.50, 2.99, "🟩 Verde Baixo", "green-low"),
        (3.00, 4.99, "🟩 Verde Médio", "green-medium"),
        (5.00, 9.99, "🟩 Verde Alto", "green-high"),
        (10.00, 19.99, "🟩 Super Verde", "green-super"),
        (20.00, 99.99, "🟩 Mega Verde", "green-mega"),
        (100.00, 999.99, "🟩 Ultra Verde", "green-ultra"),
        (1000.00, float('inf'), "🟩 Alfa Verde", "green-alpha")
    ]
    
    # Estratégia de proteção
    PROTECTION_STRATEGY = {
        "red": 1.2,
        "green-low": 1.5,
        "green-medium": 2.0,
        "green-high": 2.5,
        "green-super": 3.0,
        "green-mega": 4.0,
        "green-ultra": 5.0,
        "green-alpha": 10.0
    }
    
    # Configurações de análise
    WARNING_THRESHOLD = 0.7  # 70% de vermelhos nos últimos 10 jogos
    TREND_ANALYSIS_WINDOW = 20
