import os


def get_data(file):
    with open(file, 'r') as file:
        return file.read()


def get_text(file):
    stream = os.popen('xmllint --html --xpath \"//body//text()\" ' + file + " 2>/dev/null")
    res = stream.read()
    return res


def get_tokenize_res(file):
    return list(map(lambda x: x[:-1], open(file, "r").readlines()))