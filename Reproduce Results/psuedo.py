import math
import sys
import time
import metapy
import pytoml

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

def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

def psuedo():
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    idx = metapy.index.make_inverted_index(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    top_k = 5
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()

    res_list = []

    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            result_dict = {}
            query.content(line.strip())

            r_list = [load_pl(cfg), load_ad(cfg), load_jm(cfg), load_dp(cfg)]

            count_dict = {}

            for ranker in r_list:

                results = ranker.score(idx, query, top_k)

                # Results object testing
                for result in results:
                    scr = result[1]
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

                    if relevance > 0:
                        try:
                            result_dict.update({result[0] : result_dict.get(result[0]) + relevance})
                            count_dict.update({result[0] : count_dict.get(result[0]) + 1})
                        except:
                            result_dict.update({result[0] : relevance})
                            count_dict.update({result[0] : 1})

            av_dict = {}

            for lecture in result_dict.keys():
                av_scr = result_dict.get(lecture) // count_dict.get(lecture)
                if av_scr > 0:
                    av_dict.update({lecture : av_scr})

            for key in av_dict.keys():
                res_list.append(str(query_num) + ' ' + str(key) + ' ' + str(av_dict.get(key)))

    write_list(res_list, 'lecture-qrels.txt')
    print('Psuedo judgements complete!')


if __name__ == '__main__':
    psuedo()
