import logging
from playwright.sync_api import sync_playwright
from GetUrls import extract_book_urls
from ExtractData import extract_book_data
from WriteCSVtoEXCEL import write_to_csv

logging.basicConfig(
    level=logging.INFO, # Mude para logging.DEBUG para ver mais detalhes
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='log.txt',
    filemode='w'
)

def run(playwright):
    """
    Main execution line, it requires no input besides the function playwright, which it is used
    to make use of all the navigation and context of execution.
    :param playwright: all the functions from the library Playwright
    """
    # Extrair URLs dos livros
    logging.info('Extracting Data')
    book_urls = extract_book_urls(playwright)
    logging.info(f'Found {len(book_urls)} URLs.') # Adicionado log de contagem de URLs
    logging.info('Preparing urls')
    # Inicializar o navegador e o contexto
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Extrair dados de cada livro
    books_data = []
    logging.info('Extracting specific data from the url list')
    for i, url in enumerate(book_urls): # Adicionado contador para URLs
        try:
            logging.info(f"Processing URL {i+1}/{len(book_urls)}: {url}") # Log de progresso
            book_data = extract_book_data(page, url)  # Passar a página existente
            books_data.append(book_data)
        except Exception as e:
            logging.error(f"Erro ao extrair dados de {url}: {e}", exc_info=True) # Log de erro mais detalhado
            # Opcional: Adicionar um registro com N/A para o livro que falhou
            books_data.append({"Título": f"Erro na URL: {url}", "Preço": "N/A", "Avaliação": "N/A",
                               "UPC": "N/A", "Tipo de Produto": "N/A", "Preço (excl. tax)": "N/A",
                               "Preço (incl. tax)": "N/A", "Taxa": "N/A", "Disponibilidade": "N/A",
                               "Número de Avaliações": "N/A"})
    # Salvar os dados em um arquivo CSV
    logging.info('Preparing CSV archive')
    if books_data: # Garante que há dados para salvar
        write_to_csv(books_data, 'livro-com-todas-as-informacoes.csv','arquivo-excel-de-libros.xlsx')
    else:
        logging.warning("No book data extracted to save to CSV/Excel.")
    logging.info("\n--- Extração de dados de todos os livros concluída. ---")
    logging.info('End of everything')
    # Fechar o contexto e o navegador
    context.close()
    browser.close()
with sync_playwright() as playwright:
    logging.info('Starting Program')
    run(playwright)
