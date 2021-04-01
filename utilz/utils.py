import os
import re


def get_data(file):
    with open(file, 'r') as file:
        return file.read()


def get_text(file):
    stream = os.popen('xmllint --html --xpath \"//body//text()\" ' + file + " 2>/dev/null")
    res = stream.read()
    return res


def get_title(file):
    stream = os.popen('xmllint --html --xpath \"//title/text()\" ' + file + " 2>/dev/null")
    res = stream.read()
    return re.sub(r"\n+", " ", res)


def get_tokenize_res(file):
    return list(map(lambda x: x[:-1], open(file, "r").readlines()))

if __name__ == '__main__':
    print(get_title("../data/doc/1.html"))