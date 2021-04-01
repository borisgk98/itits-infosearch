import os
from hw2.tokenize_lemmatize import get_normal_form
from utilz.utils import get_tokenize_res


def compute_tf():
    tf = dict()
    dir = '../data/doc-tokenize'
    limit = 100
    i = 0
    for file in os.listdir(dir):
        if i > limit:
            break
        tf_page = dict()
        i += 1
        tokenize_res = get_tokenize_res(dir + '/' + file)
        for word in tokenize_res:
            normal_form = get_normal_form(word)
            if normal_form in tf_page.keys():
                tf_page[normal_form] += 1
            else:
                tf_page[normal_form] = 1
        for key, value in tf_page.items():
            if key not in tf.keys():
                tf[key] = []
            tf_val = round(value / len(tokenize_res), 6)
            tf[key].append((file[:-5], tf_val))
        print("read tf for", file[:-5])
    return dict(sorted(tf.items()))


def write_tf(tf_map):
    file = open("tf.txt", "w")
    for word, tf_list in tf_map.items():
        file_string = word + " "
        for tf in tf_list:
            file_string += " " + tf[0] + " " + str(tf[1])
        file_string += "\n"
        file.write(file_string)
    file.close()


if __name__ == '__main__':
    tf = compute_tf()
    write_tf(tf)