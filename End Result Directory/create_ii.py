# conda activate py36

import metapy

def create_ii():
    metapy.index.make_inverted_index('config.toml')

if __name__ == '__main__':
    create_ii()
