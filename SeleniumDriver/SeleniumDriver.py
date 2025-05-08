# Dependencias necessarias
#   pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class SDriver(webdriver.Chrome):
    def __init__(self, url="", options=None, mostrar_browser=False, tempo_espera=10):
        self.erro = False
        if options is None:
            options = Options()
            if not mostrar_browser:
                options.add_argument("--headless")
            options.add_argument('--log-level=3')

        super().__init__(options=options)
        self.mostrar_browser = mostrar_browser
        self.url = url
        self.implicitly_wait(tempo_espera)
        try:
            self.get(url)
        except:
            print("\033[31mNão foi possível se conectar na url\033[m")
            self.erro = True

    def __enter__(self):
        # Ao executar with open, posso colocar qualquer coisa aqui que vai executar antes do codigo dentro do with open
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.fechar()

    def fechar(self):
        self.close()
        self.quit()

''' 
# Exemplo de uso
driver = SDriver("https://site.com/", mostrar_browser=True)
elemento = driver.find_element(By.NAME, "field")
driver.fechar()

# ou

with SDriver("https://site.com/", mostrar_browser=True) as driver:
    elemento = driver.find_element(By.NAME, "field")
'''
