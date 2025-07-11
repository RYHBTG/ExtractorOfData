import logging
from playwright.sync_api import Playwright, sync_playwright, expect, Page
from GetUrl import extract_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scrap.txt',
    filemode='w'
)

def scrape_mercado_livre(base_url: str, page) -> list:
    """Extrai URLs de produtos de múltiplas páginas do Mercado Livre."""
    all_urls = []
    max_pages: int = 5
    # Sequência específica de incrementos para as páginas
    increment_sequence = [0, 49, 97, 145, 193]  # Correspondendo às páginas 1, 2, 3, 4, 5

    for i in range(max_pages):
        increment = increment_sequence[i] if i < len(increment_sequence) else increment_sequence[-1] + (48 * (i - len(increment_sequence) + 1))
        url = base_url
        # Apenas adiciona parâmetros para páginas após a primeira
        if i > 0:
            url = f"{base_url}_Desde_{increment}_NoIndex_True"

        logging.info(f'Acessando página {i+1}: {url}')
        try:
            page.goto(url, timeout=30000)
            # Se aparecer a tela de bloqueio, clicar em 'Já tenho conta'
            try:
                if page.is_visible('text="Já tenho conta"', timeout=3000):
                    page.click('text="Já tenho conta"')
                    logging.info("Clique automático em 'Já tenho conta' realizado.")
            except Exception:
                pass
            page.wait_for_selector('.ui-search-layout', timeout=10000)

            page_urls = extract_data(page)
            all_urls.extend(page_urls)
            logging.info(f'Encontrados {len(page_urls)} itens na página {i+1}')

        except Exception as e:
            logging.error(f'Erro na página {i+1}: {str(e)}', exc_info=True)
            break

    return all_urls
