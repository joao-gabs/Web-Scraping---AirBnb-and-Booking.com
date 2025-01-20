import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = r"C:\Users\Felippe\OneDrive\Desktop\Projetos\WebScraping\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
driver.get("inserir link do site (escolhendo um destino,datas e quantidade de hóspedes no airbnb conseguimos extrair informações sobre as pousadas/hoteis, precos e links para as hospedagens)")

lista_nomes_pousada = []
lista_valores = []
lista_links = []

try:
    while True:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid= "listing-card-title"]'))
        )
        
        nomes_pousada = driver.find_elements(By.XPATH, '//div[@data-testid= "listing-card-title"]')
        lista_nomes_pousada.extend([titulo.text.strip() for titulo in nomes_pousada if titulo.text.strip()])
        valores_pousada = driver.find_elements(By.XPATH, '//span[@class="_11jcbg2"]')
        lista_valores.extend([valor.text.strip() for valor in valores_pousada if valor.text.strip()])
        links_pousada = driver.find_elements(By.XPATH, '//meta[@itemprop="url"]')
        for link in links_pousada:
            content_value = link.get_attribute('content')  
            if content_value:  
                lista_links.append(content_value)
        next_button = driver.find_element(By.XPATH, '//a[@aria-label="Próximo"]') 
        next_button.click()
        time.sleep(10)  

except Exception as e:
    print("Erro ao passar de página ou fim das páginas", e)

max_length = max(len(lista_nomes_pousada), len(lista_valores), len(lista_links))
lista_nomes_pousada.extend([""] * (max_length - len(lista_nomes_pousada)))
lista_valores.extend([""] * (max_length - len(lista_valores)))
lista_links.extend([""] * (max_length - len(lista_links)))

data = {
    'Nome da Pousada': lista_nomes_pousada,
    'Preço': lista_valores,
    'Links': lista_links
}

driver.quit()

df = pd.DataFrame(data)
df.to_csv('nomearquivo.csv', index=False, encoding='utf-8')
