import logging
from playwright.sync_api import Page

def extract_products_data(page: Page, url: str) -> dict:
    logging.info(f'Acessando item: {url}')  # Log para rastreamento
    page.goto(url, wait_until="domcontentloaded")
    # Extrair o nome do produto
    nome_produto = page.locator('.ui-pdp-title').inner_text()  # Seletor correto para o nome
    # Extrair o preço
    try:
        # Tenta pegar o preço diretamente do content
        preco = page.locator('meta[itemprop="price"]').get_attribute('content')
    except Exception as e:
        logging.warning(f'Não foi possível pegar o preço diretamente: {str(e)}')
        # Se falhar, tenta pegar o preço a partir dos elementos de texto
        reais = page.locator('.andes-money-amount__fraction').inner_text()
        centavos = page.locator('.andes-money-amount__cents').inner_text()
        preco = f"{reais},{centavos}"  # Formata o preço como "R$ 74,95"
    # Retorna um dicionário com os dados do produto
    return {
        "nome": nome_produto,
        "preco": preco
    }