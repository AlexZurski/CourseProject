# search_engine.py is the source code for search_engine.py
# It uses the ranking function deemed best by bm25_master_eval.py to retrieve
# documents that are most relevant to an entered query. It returns a
# lecture number which is then used as a lookup for the lecture dictionary.
# The ranking function is updated manually. Could automate in future.

import metapy
import create_dict

# Loads ranking function as BM25 with best k1 and b values
def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.OkapiBM25(k1 = 1.98, b = 0.42)

# Find best lecture for the query
def search_engine(user_input):

    # Load configuration file
    cfg = 'config.toml'

    # Create inverted index
    # Change to already created ii in the future
    idx = metapy.index.make_inverted_index(cfg)

    # Load ranking function
    ranker = load_ranker(cfg)

    # Choose k documents to be shown to user
    top_k = 3

    # Initialize query as blank
    query = metapy.index.Document()

    # Update query content with user input
    query.content(user_input)

    # Retrieve relevnace scores for top k documents
    results = ranker.score(idx, query, top_k)

    # Initialize empty list
    lec_list = []

    # For each result, add the lecture name to the list
    for result in results:
        lec_list.append(result[0])

    # Return the list of lecture names
    return(lec_list)

# To be run from terminal or search_engine.exe
if __name__ == '__main__':

    # Create the lecture dictionary
    # Could be stored somewhere in a text file in the future.
    lec_dict = create_dict.create_dict()

    # Set a flag to true
    flag = True

    # While the flag is true
    while flag:

        # Ask the user if they have a question
        query = input('Have a question? \n')

        # If they do not, flag = false and terminate program
        if query.lower() == 'no':
            flag = False

        # If they do, run the search engine to find best documents
        else:
            lookup = search_engine(query)

            # Print the results of running the search engine
            for lecture in lookup:
                print(lec_dict.get(lecture))
