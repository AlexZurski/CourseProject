# psuedo.py creates psuedo relevance judgements on a list of queries.
# The judgements are made by Pivoted Length, Absolute Discount, Jelinek Mercer,
# and Dirichlet Prior scoring functions.
# Biggest improvement in performance could come from improving this script.

import math
import sys
import time
import metapy
import pytoml

# Load the 4 psuedo ranking functions
def load_pl(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.PivotedLength()

def load_ad(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.AbsoluteDiscount()

def load_jm(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.JelinekMercer()

def load_dp(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.DirichletPrior()

# Write a list into a file with each element having a new line
def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

# Create psuedo judgements
def psuedo():

    # Load configuration file
    cfg = 'config.toml'

    # Create inverted index
    # Change to already created ii in the future
    idx = metapy.index.make_inverted_index(cfg)

    # Load query properties
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    query_cfg = cfg_d['query-runner']

    # Throw error if queries can't be found
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    # Keep the top k documents from each scoring function
    top_k = 5

    # Load queries
    query_path = query_cfg.get('query-path', 'queries.txt')

    # Start with query 0
    query_start = query_cfg.get('query-id-start', 0)

    # Initialize query as blank
    query = metapy.index.Document()

    # Initialize relevance judgements
    res_list = []

    # Open query list
    with open(query_path) as query_file:

        # For each query in the list
        for query_num, line in enumerate(query_file):

            # Initialize a dictionary that will hold relevance scores
            result_dict = {}

            # Initialize a dictionary that will hold how many scoring functions
            # chose a particular document
            count_dict = {}

            # Set query content to string from file
            query.content(line.strip())

            # List of ranking functions to be ran
            r_list = [load_pl(cfg), load_ad(cfg), load_jm(cfg), load_dp(cfg)]

            # For each ranking function
            for ranker in r_list:

                # Retrieve relevnace scores for top k documents
                results = ranker.score(idx, query, top_k)

                # Assign relevance based on score
                # Can be improved by different methodology
                # For each result
                for result in results:

                    # Extract the score
                    scr = result[1]

                    # Assign relevance based on score
                    relevance = 0
                    if scr > 10:
                        relevance = 5
                    elif scr > 8:
                        relevance = 4
                    elif scr > 6:
                        relevance = 3
                    elif scr > 4:
                        relevance = 2
                    elif scr > 2:
                        relevance = 1

                    # If the score is not 0
                    if relevance > 0:

                        # If dictionary already has a relevance for the document,
                        # sum the relevance and add 1 to the number of ranking
                        # functions that chose that document
                        try:
                            result_dict.update({result[0] : result_dict.get(result[0]) + relevance})
                            count_dict.update({result[0] : count_dict.get(result[0]) + 1})

                        # If the dictionary is empty, insert relevance and
                        # initialize 1
                        except:
                            result_dict.update({result[0] : relevance})
                            count_dict.update({result[0] : 1})

            # Initialize a new dictionary to get average score per document
            av_dict = {}

            # For each entry in the results dictionary
            for lecture in result_dict.keys():

                # Compute average score with integer division
                # There is no penalty for a ranking function not choosing a
                # document
                av_scr = result_dict.get(lecture) // count_dict.get(lecture)

                # Only add the score if it is greater than 0
                # May be unnecessary
                if av_scr > 0:
                    av_dict.update({lecture : av_scr})

            # For each entry in the average score dictionary
            for key in av_dict.keys():

                # Add to the list the 'query number' + 'lecture number' + 'score'
                res_list.append(str(query_num) + ' ' + str(key) + ' ' + str(av_dict.get(key)))

    # Write the psuedo relevance judgements to a text file
    write_list(res_list, 'lecture-qrels.txt')

    # print('Psuedo judgements complete!')

# For local testing
if __name__ == '__main__':
    psuedo()
