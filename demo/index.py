import dataclasses
import decimal
import hashlib
from typing import Dict, Set

import nltk
import re
import orjson
import json

from demo.utilz import execute, get_normal_form


@dataclasses.dataclass
class PageInfo:
    url: str
    title: str


@dataclasses.dataclass
class WordInfo:
    count: int
    documents: Set[str]

@dataclasses.dataclass
class Index:
    hash_index: Dict[str, PageInfo]
    reverse_index: Dict[str, WordInfo]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Index, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.hash_index = dict()
        self.reverse_index = dict()

    def __preprocessing(self, file):
        return execute('bash ./sh/preprocessing.sh %s' % (file))

    def __hash_url(self, url):
        return hashlib.md5(url.encode()).hexdigest()

    def __tokenize(self, data):
        return nltk.wordpunct_tokenize(data)

    def __curl(self, url, hash):
        out = '%s/%s.html' % ("./data/html", hash)
        execute('bash ./sh/curl.sh %s %s' % (url, out))
        return out

    def __get_title(self, file):
        return re.sub(r"\n+", " ", execute('xmllint --html --xpath \"//title/text()\" ' + file + " 2>/dev/null"))

    def index(self, url):
        hash = self.__hash_url(url)
        html_file = self.__curl(url, hash)
        self.hash_index[hash] = PageInfo(url=url, title=self.__get_title(html_file))
        preprocessing_res = self.__preprocessing(html_file)
        tokens = self.__tokenize(preprocessing_res)
        normal_forms = list(map(get_normal_form, tokens))
        for normal_form in normal_forms:
            if not normal_form in self.reverse_index.keys():
                self.reverse_index[normal_form] = WordInfo(count=0, documents=set())
            existed = self.reverse_index[normal_form]
            existed.count += 1
            existed.documents.add(hash)

    def to_json(self):
        def default(obj):
            if isinstance(obj, set):
                return list(obj)
        return orjson.dumps(index, default=default)


def __load():
    data = open("./data/index.json", "r").read()
    map = orjson.loads(data)
    index = Index()
    for key, val in map["hash_index"].items():
        index.hash_index[key] = PageInfo(val["url"], val["title"])
    for key, val in map["reverse_index"].items():
        index.reverse_index[key] = WordInfo(count=val["count"], documents=set(val["documents"]))
    return index


def __gen():
    index = Index()
    f = open("./data/urls.txt", "r")
    lines = f.readlines()
    for line in lines:
        url = line[:-1]
        print("Indexing %s" % url)
        index.index(url)
    # index.index("https://flask-russian-docs.readthedocs.io/ru/latest/quickstart.html")


    o = open("./data/index.json", "wb")
    o.write(index.to_json())


index = __load()


if __name__ == '__main__':
    __gen()