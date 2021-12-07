# create_query.py takes an excel sheet of queries and converts them into a
# list in a text file. The excel sheet can have multiple sheets, but each
# row must have a title.

import pandas as pd

# Write a list into a file with each element having a new line
def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

# Create a text file of queries from an excel sheet
def create_query():

    # Load the excel workbook
    queries = pd.ExcelFile('query.xls')

    # Retrieve each sheet in the workbook
    sheets = pd.read_excel(queries, None)

    # Initialize empty list
    q_list = []

    # For each sheet
    for sheet in sheets:

        # Retrieve the columns and rows
        cols = sheets[sheet].columns
        rows = sheets[sheet].index

        # For each column
        for col in cols:

            # For each row
            for row in rows:

                # Extract the query
                query = sheets[sheet][col][row]

                # If the query is not NaN, add to list
                if not pd.isna(query):
                    q_list.append(query)

    # Write list to text file
    write_list(q_list, 'query.txt')

# For local testing
if __name__ == '__main__':
    create_query()
