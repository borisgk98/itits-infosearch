from utilz.const import limit as LIMIT
from hw3.search import read_index
from math import log


def compute_idf():
    documents_number = LIMIT
    token_document_map = dict()
    index = read_index("../hw3/index.txt")
    for element, pages in index.items():
        token_document_map[element] = round(log(documents_number / len(pages)), 6)
    return token_document_map


def write_idf(idf_map):
    file = open("idf.txt", "w")
    for word, idf in idf_map.items():
        file_string = word + " " + str(idf)
        file_string += "\n"
        file.write(file_string)
    file.close()


if __name__ == '__main__':
    tf = compute_idf()
    write_idf(tf)