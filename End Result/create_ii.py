# create_ii.py creates an inverted index
# Currently useless as search_engine.py and bm25_eval.py create
# an inverted index. In future, have them point to what is created by this.

import metapy

# Create inverted index out of corpus
def create_ii():

    # Create inverted index
    metapy.index.make_inverted_index('config.toml')

# For local testing
if __name__ == '__main__':
    create_ii()
