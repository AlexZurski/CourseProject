# create_vocab.py combines all words in the list of queries with the
# original language model to create a new language model for better text splitting.
# Once a better language model is constructed, maybe from scraping textbooks,
# this will not be needed. Also, the queries are added to the end, making them
# the least popular words, which is not always the case esp. in a dataset
# focusing on them.
# Python 3.6 or later is required as dictionaries keep their order, which
# is important because the word splitting package requires the words to be in
# order of most popular to least popular.

import re
import string

# Write a list into a file with each element having a new line
def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

# Merge every word in the list of queries with the language model
def create_vocab():

    # Read all the queries
    with open('query.txt') as f:
        queries = f.read()

    # Remove delimiters
    queries = re.sub('\s+', ' ', queries)

    # Turn all to lowercase
    queries = queries.lower()

    # Remove punctuation
    queries = queries.translate(str.maketrans('', '', string.punctuation))

    # Split the strin into a list
    queries = queries.split()

    # Read all words in the language model
    with open('allwords.txt') as f:
        allwords = f.read()

    # Remove delimiters
    allwords = re.sub('\s+', ' ', allwords)

    # Split the strin into a list
    allwords = allwords.split()

    # Create two dictionaries, one for the language model and one for the
    # queries
    all_dict = dict.fromkeys(allwords)
    q_dict = dict.fromkeys(queries)

    # Update the language model dictionary with the queries
    # If a word is in both the queries and the language model, it won't be
    # counted twice
    all_dict.update(q_dict)

    # Move all words into a list
    n_list = []

    # Since the dictionary is ordered by inseration, the list will be
    # correctly ordered
    for words in all_dict.keys():
        n_list.append(words)

    # Write the new vocabulary
    write_list(n_list, 'qallwords.txt')

# For local testing
if __name__ == '__main__':
    create_vocab()
