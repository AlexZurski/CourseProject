# conda activate py36

import pandas as pd

def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

def create_query():
    queries = pd.ExcelFile('query.xls')

    sheets = pd.read_excel(queries, None)

    q_list = []

    for sheet in sheets:
        cols = sheets[sheet].columns
        rows = sheets[sheet].index
        for col in cols:
            for row in rows:
                query = sheets[sheet][col][row]
                if not pd.isna(query):
                    q_list.append(query)

    write_list(q_list, 'query.txt')

if __name__ == '__main__':
    create_query()
