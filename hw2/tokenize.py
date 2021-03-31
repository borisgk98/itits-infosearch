import os
import nltk
from utilz.const import limit as LIMIT

def preprocessing(file):
    stream = os.popen('bash ./get-raw-data-and_preprocess-single.sh ' + file)
    res = stream.read()
    return res

def tokenize(data):
    return nltk.wordpunct_tokenize(data)


def write(result, file):
    index_txt = open(file, "w")
    pattern = "%s\n"
    for word in result:
        index_txt.write(pattern % word)
    index_txt.close()


if __name__ == '__main__':
    index = dict()
    dir = '../data/doc/'
    outdir = '../data/doc-tokenize/'
    i = 0
    for file in os.listdir(dir):
        if i > LIMIT:
            break
        i += 1
        text = preprocessing(dir + file)
        tokenize_res = tokenize(text)
        write(tokenize_res, outdir + file[:-5] + ".txt")
        print("end of tokenize doc ", file)

