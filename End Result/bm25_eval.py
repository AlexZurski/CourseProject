# bm25_eval.py is used by bm25_master_eval.py to test the performance of the BM25
# ranking function over a range of values. This script returns the performance
# in ndcg@k for a single value of k1 and b.

import math
import sys
import time
import metapy
import pytoml

# Loads ranking function as BM25 with inputted k1 and b values
def load_ranker(cfg_file, k1s, bs):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.OkapiBM25(k1 = k1s, b = bs)

# Returns a ndcg@k score for a single BM25 ranking function
def bm25_eval(k1, b):

    # Load configuration file
    cfg = 'config.toml'

    # Create inverted index
    # Change to already created ii in the future
    idx = metapy.index.make_inverted_index(cfg)

    # Load ranking function
    ranker = load_ranker(cfg, k1, b)

    # Initialize evaluation method
    ev = metapy.index.IREval(cfg)

    # Load query properties
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    query_cfg = cfg_d['query-runner']

    # Throw error if queries can't be found
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    # Choose the k of ndcg@k
    top_k = 10

    # Load queries
    query_path = query_cfg.get('query-path', 'queries.txt')

    # Start with query 0
    query_start = query_cfg.get('query-id-start', 0)

    # Initialize query as blank
    query = metapy.index.Document()

    # Initialize scoring values
    ndcg = 0.0
    num_queries = 0

    # Open query list
    with open(query_path) as query_file:

        # For each query in the list
        for query_num, line in enumerate(query_file):

            # Set query content to string from file
            query.content(line.strip())

            # Retrieve relevnace scores for top k documents
            results = ranker.score(idx, query, top_k)

            # Score against relevance judgements
            ndcg += ev.ndcg(results, query_start + query_num, top_k)

            # Increment num_queries for averaging
            num_queries+=1

        # Retrieve final score
        ndcg= ndcg / num_queries

    # Return final score
    return(ndcg)

# Used to test locally
if __name__ == '__main__':
    bm25_eval(1.98, 0.42)
