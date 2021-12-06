# conda activate py36

import re
import string

def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')
            
def create_vocab():
    with open('query.txt') as f:
        queries = f.read()

    queries = re.sub('\s+', ' ', queries)
    queries = queries.lower()
    queries = queries.translate(str.maketrans('', '', string.punctuation))

    queries = queries.split()

    with open('allwords.txt') as f:
        allwords = f.read()

    allwords = re.sub('\s+', ' ', allwords)
    allwords = allwords.split()

    all_dict = dict.fromkeys(allwords)
    q_dict = dict.fromkeys(queries)

    all_dict.update(q_dict)

    n_list = []

    for words in all_dict.keys():
        n_list.append(words)

    write_list(n_list, 'qallwords.txt')

if __name__ == '__main__':
    create_vocab()
