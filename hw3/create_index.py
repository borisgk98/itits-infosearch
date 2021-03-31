import re
import os
from functools import cmp_to_key
from hw2.tokenize_lemmatize import get_normal_form
from utilz.utils import get_tokenize_res
from utilz.const import limit as LIMIT


class WordInfo:
    def __init__(self):
        self.documents = []
        self.general_count = 0

    def append_document_info(self, document_number, document_word_count):
        self.documents.append(document_number)
        self.general_count += document_word_count


def read_lemmatization():
    f = open("../hw2/lemmatization.txt", "r")
    lines = f.readlines()
    map = dict()
    for line in lines:
        key = None
        words = re.split('\s+', line)
        for i in range(len(words) - 1):
            if i == 0:
                key = words[i]
                map[key] = []
            else:
                map[key].append(words[i])
    return map


def get_document_index(filename):
    number = ""
    for letter in filename:
        if letter.isdigit():
            number += letter
    return int(number)


def sort_index(index):
    def comparator(x, y):
        return x[1].general_count - y[1].general_count

    return dict(sorted(index.items(), key=cmp_to_key(comparator), reverse=True))


def generate_word_map(map):
    index = dict()
    dir = '../data/doc-tokenize'
    i = 0
    for file in os.listdir(dir):
        if i > LIMIT:
            break
        i += 1
        tokenize_res = get_tokenize_res(dir + '/' + file)
        word_used = set()
        for word in tokenize_res:
            normal_form = get_normal_form(word)
            if normal_form in map.keys() and normal_form not in word_used:
                word_used.add(normal_form)
                similar_words = map[normal_form]
                count = 0
                for similar_word in similar_words:
                    count += tokenize_res.count(similar_word)
                if normal_form not in index.keys():
                    index[normal_form] = WordInfo()
                index[normal_form].append_document_info(file[:-5], count)
        print("end of reading doc ", file)
    return dict(sorted(index.items()))


def write_index(index):
    file = open("index.txt", "w")
    for word, doc_info in index.items():
        file_string = word + " "
        for doc in doc_info.documents:
            file_string += " " + str(doc)
        file_string += "\n"
        file.write(file_string)
    file.close()


def create_index():
    map = read_lemmatization()
    index = generate_word_map(map)
    sorted_index = sort_index(index)
    write_index(sorted_index)


if __name__ == '__main__':
    create_index()