import csv
import logging
import openpyxl
import pandas as pd
def write_to_csv(books_data: list, filename: str, excelname: str) -> None:
    """
    Receives all the books_data in form of a dictionary and
    format them to be written correctly in the CSV file
    :param books_data: All the data
    :param filename: Name of the file
    :return: CSV file
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        logging.info('Prepping data for conversion to CSV')
        fieldnames = books_data[0].keys()  # Obter os nomes das colunas
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Escrever o cabeçalho
        writer.writerows(books_data)  # Escrever os dados
        logging.info('Prepping data for conversion to EXCEL')
        csvd = pd.read_csv(filename)
        csvd.to_excel(excelname,index=False)
