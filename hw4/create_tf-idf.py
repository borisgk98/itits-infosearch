import re
import os


def read_tf(file):
    f = open(file, "r")
    lines = f.readlines()
    tf_map = dict()
    for line in lines:
        words = re.split('\s+', line)
        key = words[0]
        for i in range(1, len(words) - 2, 2):
            if key not in tf_map:
                tf_map[key] = []
            tf_map[key].append((words[i], words[i + 1]))
    return tf_map


def read_idf(file):
    f = open(file, "r")
    lines = f.readlines()
    idf_map = dict()
    for line in lines:
        words = re.split('\s+', line)
        idf_map[words[0]] = words[1]
    return idf_map


def compute_tf_idf():
    dir = '../data/doc-tokenize'
    files = os.listdir(dir)
    tf_data = dict(sorted(read_tf("tf.txt").items()))
    idf_data = dict(sorted(read_idf("idf.txt").items()))
    tf_idf_map = dict()
    for token, documents_tf in tf_data.items():
        tf_idf_map[token] = []
        documents_tf = dict(documents_tf)
        for file in files:
            file_key = file[:-4]
            if file_key in documents_tf.keys():
                tf = float(documents_tf[file_key])
            else:
                tf = float(0)
            if token in idf_data.keys():
                tf_idf_map[token].append((file_key, tf * float(idf_data[token])))
            else:
                print("Cannot find token %s in index!" % token)
                break
    return tf_idf_map


def write_tf_idf(tf_idf_map):
    file = open("tf_idf.txt", "w")
    for word, tf_idf_list in tf_idf_map.items():
        file_string = word + " "
        for tf in tf_idf_list:
            file_string += " " + tf[0] + " " + str(tf[1])
        file_string += "\n"
        file.write(file_string)
    file.close()


if __name__ == '__main__':
    tf_idf = compute_tf_idf()
    write_tf_idf(tf_idf)