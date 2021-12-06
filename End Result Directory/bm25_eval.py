import math
import sys
import time
import metapy
import pytoml

def load_ranker(cfg_file, k1s, bs):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.OkapiBM25(k1 = k1s, b = bs)

def bm25_eval(k1, b):
    cfg = 'config.toml'
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg, k1, b)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']

    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    ndcg = 0.0
    num_queries = 0

    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            print(query)
            results = ranker.score(idx, query, top_k)
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
        ndcg= ndcg / num_queries

    return(ndcg)

if __name__ == '__main__':
    bm25_eval(1.98, 0.42)
