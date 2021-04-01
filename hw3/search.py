import re
from hw2.tokenize_lemmatize import get_normal_form


def read_index(file):
    f = open(file, "r")
    lines = f.readlines()
    map = dict()
    for line in lines:
        words = re.split('\s+', line)
        key = words[0]
        if not key in map.keys():
            map[key] = set()
        for i in range(1, len(words) - 1):
            map[key].add(words[i])
    return map


def compute_query(query, bi_map, u_map, op):
    """Расчет выражение

    query   []                      выражение, которое нужно вычислить.
    bi_map  {"operand": f(x, y)}    бинарные операнды
    u_map   {"operand": f(x)}       унарные операнды
    op      {"operand": int}        приоритеты операндов (операнд большего приоритета высчитывается раньше)
    """
    op_stack = []
    val_stack = []
    for o in query:
        if o == "(":
            op_stack.append(o)
        elif o == ")":
            while len(op_stack) != 0 and op_stack[-1] != "(":
                last = op_stack[-1]
                if last in bi_map.keys():
                    x = val_stack[-2]
                    y = val_stack[-1]
                    val_stack = val_stack[:-2]
                    val_stack.append(bi_map[last](x, y))
                else:
                    x = val_stack[-1]
                    val_stack.pop()
                    val_stack.append(u_map[last](x))
                op_stack.pop()
            if len(op_stack) == 0:
                print("Braces error!")
                return None
            op_stack.pop()
        elif type(o) is str and (o in u_map.keys() or o in bi_map.keys()):
            while len(op_stack) != 0 and op_stack[-1] != "(" and op[op_stack[-1]] > op[o]:
                last = op_stack[-1]
                if last in bi_map.keys():
                    x = val_stack[-2]
                    y = val_stack[-1]
                    val_stack = val_stack[:-2]
                    val_stack.append(bi_map[last](x, y))
                else:
                    x = val_stack[-1]
                    val_stack.pop()
                    val_stack.append(u_map[last](x))
                op_stack.pop()
            op_stack.append(o)
        else:
            val_stack.append(o)

    while len(op_stack) != 0:
        last = op_stack[-1]
        if last in bi_map.keys():
            x = val_stack[-2]
            y = val_stack[-1]
            val_stack = val_stack[:-2]
            val_stack.append(bi_map[last](x, y))
        else:
            x = val_stack[-1]
            val_stack.pop()
            val_stack.append(u_map[last](x))
        op_stack.pop()

    if len(val_stack) != 1:
        print("WARNING! Bad query")

    return val_stack[0]


def boolean_search(query, index):
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
        if normal_form in index:
            return index[normal_form]
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


if __name__ == '__main__':
    # boolean_search("Устройство громкого оповещения", read_index())
    res, _, _ = boolean_search("(Новые области) | России", read_index("index.txt"))
    print(res)
    # print(compute_query([1, "+", "(", "-", 2, ")"], {"+": lambda x, y: x + y}, {"-": lambda x: -x}, {"+": 1, "-": 2}))