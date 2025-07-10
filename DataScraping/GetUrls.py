import logging
import re
from playwright.sync_api import Playwright
from urllib.parse import urljoin
def extract_book_urls(playwright: Playwright) -> list:
    """
    Makes a detailed extraction of all the links of the books from the URL
    :param playwright:
    :return: all_book_url (inside it has all the url's to make the extraction)
    """
    all_book_urls = []  # Lista para armazenar TODAS as URLs de livros
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Loop para percorrer 50 páginas
    for page_num in range(1, 51):
        logging.info('Prepping up pages for data extraction')
        current_listing_url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
        page.goto(current_listing_url, wait_until="domcontentloaded")
        # Encontra todos os elementos de produto na página atual
        products = page.query_selector_all('li.col-xs-6.col-sm-4.col-md-3.col-lg-3')
        if not products:
            print(f"Não foram encontrados produtos na página {page_num}. Fim da paginação.")
            break  # Sai do loop de páginas se não houver mais produtos
        # Para cada produto na página atual, extrair a URL do livro
        for product in products:
            booklink = product.query_selector('h3 > a')
            if booklink:
                logging.info('Extracting data...')
                relative_href = booklink.get_attribute('href')
                full_book_url = urljoin("http://books.toscrape.com/catalogue/", relative_href)

                # Evitar adicionar URLs duplicadas
                if full_book_url not in all_book_urls:
                    all_book_urls.append(full_book_url)
    context.close()
    browser.close()
    return all_book_urls
