
import logging
from playwright.sync_api import sync_playwright, Page
from GetUrl import extract_data
from NextPage import scrape_mercado_livre
from GetItensData import extract_products_data
import csv
import tkinter as tk
from tkinter import simpledialog

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scrap.txt',
    filemode='w'
)

def main():
    # Pop-up para o usuário digitar o nome do produto
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    produto_nome = simpledialog.askstring("Busca Mercado Livre", "Digite o nome do produto para buscar:")
    if not produto_nome:
        print("Nenhum produto informado. Encerrando.")
        return
    produto_nome_url = produto_nome.strip().replace(' ', '+')

    base_url = f"https://lista.mercadolivre.com.br/{produto_nome_url}"
    logging.info(f"Iniciando extração de URLs de produtos para: {produto_nome}")

    # Abre o navegador Playwright, faz login e extrai URLs
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Extrai todas as URLs de produtos das páginas já autenticado, passando o page
        all_urls = scrape_mercado_livre(base_url, page)
        logging.info(f"Total de URLs coletadas: {len(all_urls)}")

        # Extrai dados dos produtos
        produtos = []
        for url in all_urls:
            try:
                dados = extract_products_data(page, url)
                produtos.append(dados)
                logging.info(f"Produto extraído: {dados}")
            except Exception as e:
                logging.error(f"Erro ao extrair dados do produto {url}: {str(e)}")
        context.close()
        browser.close()

    # Escreve os dados em um arquivo CSV
    with open("produtos.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["nome", "preco"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto)
    print(f"Dados de {len(produtos)} produtos salvos em produtos.csv")


if __name__ == "__main__":
    main()

