# cd desktop/cs410/project
# conda activate py36
# python create_textdata.py
import create_query
import create_vocab
import create_bow
import create_corpus
import create_ii
import time

if __name__ == '__main__':

    # # start timing
    # # for testing only
    # start = time.time()

    print('Creating queries...')
    create_query.create_query()
    print('Done!')

    print('Creating vocab...')
    create_vocab.create_vocab()
    print('Done!')

    print('Creating bag of words...')
    create_bow.create_bow()
    print('Done!')

    print('Creating corpus...')
    create_corpus.create_corpus()
    print('Done!')

    print('Creating inverted index...')
    create_ii.create_ii()
    print('Done!')

    # # time how long this function takes
    # # for testing only
    # end = time.time()
    # print(end - start)
