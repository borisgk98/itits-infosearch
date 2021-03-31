import os
import nltk
import pymorphy2
from utilz.utils import get_data

# nltk.download('all')
# nltk.download('wordnet')

raw_file = "out.txt"


def preprocessing():
    os.system("bash ./get-raw-data-and_preprocess.sh " + raw_file)


def tokenize(data):
    return nltk.wordpunct_tokenize(data)


def write_tokenization_result(result):
    index_txt = open("tokenization.txt", "w")
    pattern = "%s\n"
    for word in result:
        index_txt.write(pattern % word)
    index_txt.close()

# Lemmatization
morph = pymorphy2.MorphAnalyzer()


def lemmatization(tokenization_result):
    result = dict()
    for word in tokenization_result:
        normal_form = get_normal_form(word)
        if not normal_form in result:
            result[normal_form] = []
        result[normal_form].append(word)
    return result


def get_normal_form(word):
    p = morph.parse(word)[0]
    if p.normalized.is_known:
        normal_form = p.normal_form
    else:
        normal_form = word.lower()
    return normal_form


def write_lemmatization_result(lemmatization_result):
    file = open("lemmatization.txt", "w")
    for lemma, tokens in lemmatization_result.items():
        file_string = lemma + " "
        for token in tokens:
            file_string += token + " "
        file_string += "\n"
        file.write(file_string)
    file.close()


if __name__ == '__main__':
    data = get_data(raw_file)
    tokenization_res = tokenize(data)
    write_tokenization_result(tokenization_res)
    lemmatization_res = lemmatization(tokenization_res)
    write_lemmatization_result(lemmatization_res)

