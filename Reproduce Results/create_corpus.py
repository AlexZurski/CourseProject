# conda activate py36

import os
import shutil

def dir_up():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)

def create_corpus():
    if ('courses' in os.listdir()):
        shutil.rmtree('courses')

    os.mkdir('courses')

    os.chdir('test_data')

    corpus = []

    for doc in os.listdir():
        with open(doc) as f:
            line = f.read()
        corpus.append(line)

    dir_up()

    os.chdir('courses')
    write_list(corpus, 'courses.dat')

    line_type = 'type = "line-corpus"'

    write_list(line_type, 'line.toml')

    dir_up()

if __name__ == '__main__':
    create_corpus()
