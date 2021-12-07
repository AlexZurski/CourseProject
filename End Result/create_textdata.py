# create_textdata.py creates a list of queries, a vocabulary, a bag of words
# representation for each data file, a corpus, and an inverted index for a
# data set of lecture pdfs
# It does so by calling each of the python scripts below. Since each script relies
# on the output of the ones above it, it is helpful to have a centralized
# script.

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

    # Create list of queries
    print('Creating queries...')
    create_query.create_query()
    print('Done!')

    # Create vocab
    print('Creating vocab...')
    create_vocab.create_vocab()
    print('Done!')

    # Create bag of words for each data file
    print('Creating bag of words...')
    create_bow.create_bow()
    print('Done!')

    # Create corpus
    print('Creating corpus...')
    create_corpus.create_corpus()
    print('Done!')

    # Create inverted index
    print('Creating inverted index...')
    create_ii.create_ii()
    print('Done!')

    # # time how long this function takes
    # # for testing only
    # end = time.time()
    # print(end - start)
