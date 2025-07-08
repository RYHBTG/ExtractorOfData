
import re
import csv
from playwright.sync_api import Playwright, sync_playwright, expect
from urllib.parse import urljoin


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    all_book_urls = []  # Lista para armazenar TODAS as URLs de livros, de todas as páginas

    # Loop para percorrer 50 páginas
    for page_num in range(1, 51):
        current_listing_url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
        page.goto(current_listing_url, wait_until="domcontentloaded")  # Espera o DOM carregar
        page.wait_for_timeout(300)

        # Encontra todos os elementos de produto na página atual
        products = page.query_selector_all('li.col-xs-6.col-sm-4.col-md-3.col-lg-3')

        if not products:
            print(f"Não foram encontrados produtos na página {page_num}. Fim da paginação.")
            break  # Sai do loop de páginas se não houver mais produtos

        # Para cada produto na página atual, extrair a URL do livro
        for product in products:
            booklink = product.query_selector('h3 > a')
            if booklink:
                relative_href = booklink.get_attribute('href')
                full_book_url = urljoin("http://books.toscrape.com/catalogue/", relative_href)

                # Evitar adicionar URLs duplicadas
                if full_book_url not in all_book_urls:
                    all_book_urls.append(full_book_url)

    # --- Parte 2: Processar cada URL de livro coletada ---
    books_data = []  # Lista para armazenar os dados dos livros

    for j, url in enumerate(all_book_urls):
        try:
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
            product_type = page.locator(
                'table.table-striped tr:has(th:text-is("Product Type")) > td').text_content().strip()
            price_excl_tax = page.locator(
                'table.table-striped tr:has(th:text-is("Price (excl. tax)")) > td').text_content().strip()
            price_incl_tax = page.locator(
                'table.table-striped tr:has(th:text-is("Price (incl. tax)")) > td').text_content().strip()
            tax = page.locator('table.table-striped tr:has(th:text-is("Tax")) > td').text_content().strip()
            availability = page.locator(
                'table.table-striped tr:has(th:text-is("Availability")) > td').text_content().strip()
            number_of_reviews = page.locator(
                'table.table-striped tr:has(th:text-is("Number of reviews")) > td').text_content().strip()

            # Armazenar os dados do livro
            books_data.append({
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
            })

        except Exception as e:
            print(f"Erro ao extrair dados de {url}: {e}")

    # Salvar os dados em um arquivo CSV
    with open('books_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = books_data[0].keys()  # Obter os nomes das colunas
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()  # Escrever o cabeçalho
        writer.writerows(books_data)  # Escrever os dados

    print("\n--- Extração de dados de todos os livros concluída. ---")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
