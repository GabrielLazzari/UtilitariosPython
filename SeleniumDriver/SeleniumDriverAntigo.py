# Dependencias necessarias
#   pip install selenium
#   pip install webdriver-manager

from os.path import isfile
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SDriver(webdriver.Chrome):
    def __init__(self, url="", options=None, mostrar_browser=False, tempo_espera=10):
        self.erro = False
        if options is None:
            options = Options()
            if not mostrar_browser:
                options.add_argument("--headless")
            options.add_argument('--log-level=3')

        if not isfile("metadados.db"): open("metadados.db", "w").close()

        with sqlite3.connect("metadados.db") as conexao:
            self.conexao = conexao
            self.cursor = conexao.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS metadados (nome char(100), valor char(250));")

        novo_caminho = self.atualizar_driver()
        service = Service(novo_caminho)

        super().__init__(service=service, options=options)
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

    def retornar_caminho(self):
        self.cursor.execute("SELECT valor FROM metadados WHERE nome = 'caminho_webdriver'")
        return caminho if (caminho := self.cursor.fetchone()) is None else caminho[0]

    def atualizar_caminho(self, novo_caminho):
        self.cursor.execute("SELECT valor FROM metadados WHERE nome = 'caminho_webdriver'")
        if self.cursor.fetchone() is not None:
            self.cursor.execute(f"UPDATE metadados SET valor = '{novo_caminho}' WHERE nome = 'caminho_webdriver'")
        else:
            self.cursor.execute(f"INSERT INTO metadados VALUES('caminho_webdriver', '{novo_caminho}')")
        self.conexao.commit()

    def validar_novo_caminho(self, caminho):
        try:
            if not caminho.endswith("chromedriver.exe"):
                caminho = re.split(r'\\|/', caminho)
                caminho = "\\".join(caminho[:-1]) + "\\chromedriver.exe"
        except:
            pass

        return caminho

    def baixar_driver(self):
        try:
            novo_caminho = self.validar_novo_caminho(ChromeDriverManager().install())
            return novo_caminho
        except:
            return ""

    def atualizar_driver(self):
        try:
            caminho = self.retornar_caminho()
            if caminho is None:
                raise Exception
            return caminho
        except:
            caminho = self.baixar_driver()
            self.atualizar_caminho(caminho)
            return caminho


''' 
# Exemplo de uso
driver = SDriver("https://site.com/", mostrar_browser=True)
elemento = driver.find_element(By.NAME, "field")
driver.fechar()

# ou

with SDriver("https://site.com/", mostrar_browser=True) as driver:
    elemento = driver.find_element(By.NAME, "field")
'''
