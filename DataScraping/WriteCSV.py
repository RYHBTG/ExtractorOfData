
import csv
def write_to_csv(books_data: list, filename: str) -> None:
    """
    Receives all the books_data in form of a dictionary and
    format them to be written correctly in the CSV file
    :param books_data: All the data
    :param filename: Name of the file
    :return: CSV file
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = books_data[0].keys()  # Obter os nomes das colunas
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Escrever o cabeçalho
        writer.writerows(books_data)  # Escrever os dados