import os
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def execute(cmd):
    print("execute command: %s" % cmd)
    stream = os.popen(cmd)
    res = stream.read()
    return res


def get_normal_form(word):
    p = morph.parse(word)[0]
    if p.normalized.is_known:
        normal_form = p.normal_form
    else:
        normal_form = word.lower()
    return normal_form


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