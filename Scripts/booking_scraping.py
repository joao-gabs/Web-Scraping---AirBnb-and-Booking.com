import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

url = ''' url dentro do booking.com escolhendo uma cidade e uma determinada data de check-in e check-out'''
page = requests.get(url, headers = headers)
soup = BeautifulSoup(page.text,'html.parser')

nomes_pousada = [nomes.get_text(strip=True) for nomes in soup.find_all(['h3', 'div'], {'data-testid': 'title'})]
valores = [valor.get_text(strip=True) for valor in soup.find_all('span', {'data-testid': 'price-and-discounted-price'})]
distancia_praia = [d.get_text(strip=True) for d in soup.find_all('span', string=lambda text: text and ('m da praia' in text.lower() or 'beira-mar' in text.lower()))]
cidades = [nome.get_text(strip=True) for nome in soup.find_all('span', {'data-testid': 'address'})]
numero_avaliacoes = [a.get_text(strip=True) for a in soup.find_all('div', string=lambda text: text and ('avaliações' in text.lower() and not text.lower().startswith('com base')))]
tipo_acomodacao = [t.get_text(strip = True) for t in soup.find_all('h4', class_ ="abf093bdfe e8f7c070a7")]




max_length = max(len(nomes_pousada), len(valores), len(distancia_praia), len(cidades), len(numero_avaliacoes), len(tipo_acomodacao))
nomes_pousada.extend([''] * (max_length - len(nomes_pousada)))
valores.extend([''] * (max_length - len(valores)))
distancia_praia.extend([''] * (max_length - len(distancia_praia)))
cidades.extend([''] * (max_length - len(cidades)))
numero_avaliacoes.extend([''] * (max_length - len(numero_avaliacoes)))
tipo_acomodacao.extend([''] * (max_length - len(tipo_acomodacao)))


data = {
    'Nome da Pousada': nomes_pousada,
    'Preço': valores,
    'Distância da Praia': distancia_praia,
    'Cidade': cidades,
    'Número de Avaliações': numero_avaliacoes,
    'Tipo de Acomodação': tipo_acomodacao
}

df = pd.DataFrame(data)
df.replace('', 'Sem Avaliação', inplace=True)

df.to_csv('nomedoseuarquivo.csv', index=False, encoding='utf-8')

