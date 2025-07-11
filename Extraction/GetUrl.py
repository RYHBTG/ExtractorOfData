import re
import csv
import time
from playwright.sync_api import Playwright, sync_playwright, expect, Page
import logging

def extract_data(page: Page) -> list:
    """
    Faz uma extração detalhada de todos os links dos produtos da URL.
    :param page: Página do Playwright onde a extração será realizada.
    :return: all_items_url (contém todas as URLs dos produtos).
    """
    all_items_url = set()  # Usar um conjunto para evitar duplicatas
    try:
        # Esperar até que os produtos estejam carregados
        page.wait_for_selector('.ui-search-layout__item', timeout=10000)
        products = page.query_selector_all('.ui-search-layout__item')
        if not products:
            logging.info("Não foram encontrados produtos na página. Fim da paginação.")
        else:
            for product in products:
                url_product = product.query_selector('h3 > a')
                if url_product:
                    # Obter o valor da URL corretamente
                    relative_href = url_product.get_attribute('href')
                    if relative_href:
                        all_items_url.add(relative_href)  # Adiciona ao conjunto
                        logging.info(f'URL encontrada: {relative_href}')  # Log da URL encontrada
    except Exception as e:
        logging.error(f'Erro durante a extração de dados: {str(e)}', exc_info=True)
    return list(all_items_url)  # Retorna como lista
