import metapy
import create_dict

def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.OkapiBM25(k1 = 1.98, b = 0.42)

def search_engine(user_input):
    cfg = 'config.toml'
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)

    top_k = 3

    query = metapy.index.Document()

    query.content(user_input)

    results = ranker.score(idx, query, top_k)

    lec_list = []

    for result in results:
        lec_list.append(result[0])

    return(lec_list)

if __name__ == '__main__':
    lec_dict = create_dict.create_dict()
    flag = True

    while flag:
        query = input('Have a question? \n')
        if query.lower() == 'no':
            flag = False
        else:
            lookup = search_engine(query)

            for lecture in lookup:
                print(lec_dict.get(lecture))
