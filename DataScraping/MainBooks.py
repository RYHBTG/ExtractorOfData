from playwright.sync_api import sync_playwright
from GetUrls import extract_book_urls
from ExtractData import extract_book_data
from WriteCSVtoEXCEL import write_to_csv
def run(playwright):
    """
    Main execution line, it requires no input besides the function playwright, which it is used
    to make use of all the navigation and context of execution.
    :param playwright: all the functions from the library Playwright
    """
    # Extrair URLs dos livros
    book_urls = extract_book_urls(playwright)
    # Inicializar o navegador e o contexto
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Extrair dados de cada livro
    books_data = []
    for url in book_urls:
        try:
            book_data = extract_book_data(page, url)  # Passar a página existente
            books_data.append(book_data)
        except Exception as e:
            print(f"Erro ao extrair dados de {url}: {e}")
    # Salvar os dados em um arquivo CSV
    write_to_csv(books_data, 'livrodedados.csv','converted-csv.xlsx')
    print("\n--- Extração de dados de todos os livros concluída. ---")
    # Fechar o contexto e o navegador
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)