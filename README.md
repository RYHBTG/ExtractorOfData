
# Books to Scrape

Este projeto é um web scraper que extrai informações sobre livros do site [Books to Scrape](http://books.toscrape.com/). O scraper coleta dados como título, preço, avaliação, UPC, tipo de produto, preços com e sem taxa, disponibilidade e número de avaliações. Os dados extraídos são salvos em um arquivo CSV.

## Estrutura do Projeto

O projeto é dividido em três módulos principais:

1. **`url_extractor.py`**: Responsável por extrair as URLs dos livros a partir das páginas do site.
2. **`data_extractor.py`**: Responsável por extrair os dados de cada livro a partir das URLs coletadas.
3. **`csv_writer.py`**: Responsável por salvar os dados extraídos em um arquivo CSV.
4. **`main.py`**: O ponto de entrada do programa que orquestra a execução dos outros módulos.

## Requisitos

Para executar este projeto, você precisará ter o Python 3.x instalado, além das seguintes bibliotecas:

- `playwright`: Para interagir com o navegador e realizar a extração de dados.
- `csv`: Para salvar os dados em um arquivo CSV (já incluído na biblioteca padrão do Python).

Você pode instalar o Playwright usando o seguinte comando:

```bash
pip install playwright
pip install pandas openpyxl
```
Após a instalação, você também precisará instalar os navegadores suportados:  
```bash
playwright install
```
Como Usar
Clone este repositório para sua máquina local:
```bash
git clone https://github.com/seu_usuario/seu_repositorio.git
cd seu_repositorio
```
Para visualizar o que busca extrair ou realizar basta utilizar o código abaixo, retire os () e também substitua o texto de dentro:
```bash
playwright codegen (link-do-seu-site.com)
```
Execute o script main.py:
```bash
python main.py
```
Após a execução, um arquivo chamado books_data.csv será gerado no diretório atual, contendo os dados extraídos dos livros.
## Descrição dos Módulos
### url_extractor.py
- Este módulo contém a função extract_book_urls, que percorre as páginas do site e coleta as URLs dos livros. Ele utiliza o Playwright para navegar pelas páginas e extrair os links.

### data_extractor.py
- Este módulo contém a função extract_book_data, que recebe uma URL de um livro e extrai os dados relevantes. Ele utiliza o Playwright para abrir a página do livro e coletar as informações.

### csv_writer.py
- Este módulo contém a função write_to_csv, que recebe uma lista de dicionários (dados dos livros) e salva essas informações em um arquivo CSV.

### main.py
- Este é o ponto de entrada do programa. Ele orquestra a execução dos outros módulos, chamando as funções para extrair URLs, coletar dados e salvar os resultados em um arquivo CSV.

### Bibliotecas utilizadas para desenvolvimento:
```bash
import csv // 'Desenvolvimento e exportação para arquivos csv'
from playwright.sync_api import Playwright, sync_playwright, expect // 'Funções de playwright'
from urllib.parse import urljoin // 'Melhor manipulação de urls, para tratamento, requisições, etc.'
```
