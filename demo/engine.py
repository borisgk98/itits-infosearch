import re

from demo.utilz import compute_query, get_normal_form
from demo.index import index


def boolean_search(query):
    query = query.strip()
    func_bi = {
        "&": lambda x, y: x & y,
        "|": lambda x, y: x | y
    }
    func_p = {
        "&": 1,
        "|": 2
    }

    operands = ("(", ")", "&", "|")
    res_query = []
    parsed_query = []
    parsed_query_words = []
    last = None

    def get_or_default(x):
        normal_form = get_normal_form(x)
        if normal_form in index.reverse_index:
            return index.reverse_index[normal_form].documents
        else:
            return set()

    for s in re.split("\s+", query):
        if s[0] == "(":
            if last is not None and last not in operands:
                res_query.append("&")
                parsed_query.append("&")
            res_query.append("(")
            res_query.append(get_or_default(s[1:]))

            parsed_query.append("(")
            parsed_query.append(s[1:])

            parsed_query_words.append(s[1:])
        elif s[-1] == ")":
            if last is not None and last not in operands:
                res_query.append("&")
            res_query.append(get_or_default(s[:-1]))
            res_query.append(")")

            parsed_query.append(s[:-1])
            parsed_query.append(")")

            parsed_query_words.append(s[:-1])
        elif s in operands:
            res_query.append(s)
            parsed_query.append(s)
        else:
            if (last is not None and last not in operands) or (last is not None and last == ")"):
                res_query.append("&")
                res_query.append(get_or_default(s))

                parsed_query.append("&")
                parsed_query.append(s)

                parsed_query_words.append(s)
            else:
                res_query.append(get_or_default(s))
                parsed_query.append(s)
                parsed_query_words.append(s)
        last = s
    return compute_query(res_query, func_bi, {}, func_p), parsed_query, parsed_query_words