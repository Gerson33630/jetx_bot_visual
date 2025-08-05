from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class JetXScraper:
    def __init__(self):
        self.options = Options()
        self._setup_options()
        
    def _setup_options(self):
        """Configura as opções do navegador"""
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
    
    def get_current_multiplier(self):
        """Obtém o multiplicador atual"""
        driver = webdriver.Chrome(options=self.options)
        try:
            driver.get("https://www.elephant.bet/pt/games/jetx")
            time.sleep(5)
            
            selectors = [
                (By.CSS_SELECTOR, ".multiplier-display .current-value"),
                (By.CSS_SELECTOR, ".current-multiplier span"),
                (By.XPATH, "//div[contains(@class, 'multiplier')]//span")
            ]
            
            for by, selector in selectors:
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    value_text = element.text.replace('x', '').strip()
                    return float(value_text)
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"Erro durante scraping: {str(e)}")
            return None
        finally:
            driver.quit()
