import logging
from playwright.sync_api import Playwright, Page


def extract_book_data(page: Page, url: str) -> dict:
    """
    Extract data from the url's that it receives
    :param page: A página do Playwright já inicializada.
    :param url: A URL do livro a ser extraído.
    :return: Dicionário com os dados do livro.
    """
    logging.info(f'Going to next item: {url}')  # Adicionado URL para melhor rastreamento
    page.goto(url, wait_until="domcontentloaded")
    # Extração de dados
    logging.info('Extraction of main data')
    title = page.locator('.product_main h1').text_content().strip()
    price = page.locator('.product_main .price_color').text_content().strip()

    rating_element = page.locator('.product_main .star-rating')
    class_attribute = rating_element.get_attribute('class')
    found_rating = "N/A"

    logging.debug(f"Rating element found: {rating_element is not None}")  # Log de depuração
    logging.debug(f"Class attribute: {class_attribute}")  # Log de depuração

    if class_attribute:
        rating_classes = class_attribute.split()
        possible_ratings = ["One", "Two", "Three", "Four", "Five"]

        # Tenta encontrar a avaliação na lista de classes
        found_rating_temp = next((r for r in rating_classes if r in possible_ratings), None)

        if found_rating_temp:
            found_rating = found_rating_temp
            logging.info(f"Rating extracted: {found_rating}")  # Log de sucesso
        else:
            logging.warning(f"No valid rating class found in '{class_attribute}' for URL: {url}")  # Log de aviso
            found_rating = "N/A"  # Mantém N/A se nenhuma classe válida for encontrada
    else:
        logging.warning(f"Star rating element or its class attribute not found for URL: {url}")  # Log de aviso
        found_rating = "N/A"  # Mantém N/A se o atributo de classe não existir

    upc = page.locator('table.table-striped tr:has(th:text-is("UPC")) > td').text_content().strip()
    product_type = page.locator('table.table-striped tr:has(th:text-is("Product Type")) > td').text_content().strip()
    price_excl_tax = page.locator('table.table-striped tr:has(th:text-is("Price (excl. tax)")) > td').text_content().strip()
    price_incl_tax = page.locator('table.table-striped tr:has(th:text-is("Price (incl. tax)")) > td').text_content().strip()
    tax = page.locator('table.table-striped tr:has(th:text-is("Tax")) > td').text_content().strip()
    availability = page.locator('table.table-striped tr:has(th:text-is("Availability")) > td').text_content().strip()
    number_of_reviews = page.locator('table.table-striped tr:has(th:text-is("Number of reviews")) > td').text_content().strip()
    logging.info('Extraction made with success, sending new data')
    return {
        "Título": title, "Preço": price, "Avaliação": found_rating, "UPC": upc, "Tipo de Produto": product_type,
        "Preço (excl. tax)": price_excl_tax,
        "Preço (incl. tax)": price_incl_tax, "Taxa": tax, "Disponibilidade": availability,
        "Número de Avaliações": number_of_reviews
    }
