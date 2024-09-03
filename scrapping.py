import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL específica da busca
url = "https://www.google.com/search?q=ar+condicionado+lg+dual+inverter+voice+9000+BTUs"

# Defina cabeçalhos para a requisição (importante para evitar bloqueios)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Faça a requisição HTTP para o Google
response = requests.get(url, headers=headers)

# Verifique se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parse do conteúdo HTML usando BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontre os blocos que contêm os resultados de busca
    search_results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')

    # Coletar resultados
    results = []
    for result in search_results:
        # Extrair o texto relevante de cada resultado
        text = result.get_text()

        # Procura o atributo 'data-dtld' para capturar o nome da loja
        parent = result.find_parent('div')
        if parent and parent.has_attr('data-dtld'):
            store_name = parent['data-dtld']
        else:
            store_name = "Desconhecida"

        # Captura o link associado
        link_tag = parent.find('a', href=True) if parent else None
        link = link_tag['href'] if link_tag else "Link não disponível"

        if "R$" in text:  # Verifique se há um preço no texto
            results.append({
                "Loja": store_name,
                "Resultado": text,
                "Link": link
            })

    # Converter a lista de resultados em um DataFrame do pandas
    if results:  # Verifica se há resultados antes de criar a planilha
        df = pd.DataFrame(results)
        # Salvar em uma planilha Excel
        df.to_excel("resultados_busca_google.xlsx", index=False)
        print("Resultados salvos em 'resultados_busca_google.xlsx'.")
    else:
        print("Nenhum resultado relevante foi encontrado.")
else:
    print(f"Falha ao realizar a requisição: {response.status_code}")
