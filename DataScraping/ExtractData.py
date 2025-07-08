from playwright.sync_api import Playwright, Page


def extract_book_data(page: Page, url: str) -> dict:
    """
    Extract data from the url's that it receives
    :param page: A página do Playwright já inicializada.
    :param url: A URL do livro a ser extraído.
    :return: Dicionário com os dados do livro.
    """
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(300)  # Aguardar o carregamento da página

    # Extração de dados
    title = page.locator('.product_main h1').text_content().strip()
    price = page.locator('.product_main .price_color').text_content().strip()

    rating_element = page.locator('.product_main .star-rating')
    class_attribute = rating_element.get_attribute('class')
    found_rating = "N/A"
    if class_attribute:
        rating_classes = class_attribute.split()
        possible_ratings = ["One", "Two", "Three", "Four", "Five"]
        found_rating = next((r for r in rating_classes if r in possible_ratings), "N/A")

    upc = page.locator('table.table-striped tr:has(th:text-is("UPC")) > td').text_content().strip()
    product_type = page.locator('table.table-striped tr:has(th:text-is("Product Type")) > td').text_content().strip()
    price_excl_tax = page.locator(
        'table.table-striped tr:has(th:text-is("Price (excl. tax)")) > td').text_content().strip()
    price_incl_tax = page.locator(
        'table.table-striped tr:has(th:text-is("Price (incl. tax)")) > td').text_content().strip()
    tax = page.locator('table.table-striped tr:has(th:text-is("Tax")) > td').text_content().strip()
    availability = page.locator('table.table-striped tr:has(th:text-is("Availability")) > td').text_content().strip()
    number_of_reviews = page.locator(
        'table.table-striped tr:has(th:text-is("Number of reviews")) > td').text_content().strip()

    return {
        "Título": title,
        "Preço": price,
        "Avaliação": found_rating,
        "UPC": upc,
        "Tipo de Produto": product_type,
        "Preço (excl. tax)": price_excl_tax,
        "Preço (incl. tax)": price_incl_tax,
        "Taxa": tax,
        "Disponibilidade": availability,
        "Número de Avaliações": number_of_reviews
    }
