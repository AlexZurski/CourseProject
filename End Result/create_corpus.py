# create_corpus.py takes all text data extracted from create_bow.py and
# creates a singular .dat file with each text file being put on one line

import os
import shutil

# Move to the parent of the current directory
def dir_up():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

# Write a list into a file
# Each item has its own line
def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)

# Turn a data set of text files into a corpus
def create_corpus():

    # Delete corpus if it already exists
    # Less damaging solution to be looked for in the future
    if ('courses' in os.listdir()):
        shutil.rmtree('courses')

    # Create a directory to store corpus
    os.mkdir('courses')

    # Move into directory containing text data
    os.chdir('test_data')

    # Initialize empty list
    corpus = []

    # For each text document
    for doc in os.listdir():

        # Open the file and read it
        with open(doc) as f:
            line = f.read()

        # Add file lies to list
        corpus.append(line)

    # Return to directory containing corpus directory
    dir_up()

    # Change into the corpus directory
    os.chdir('courses')

    # Write the corpus
    write_list(corpus, 'courses.dat')

    # Additionally write corpus information into line.toml
    line_type = 'type = "line-corpus"'
    write_list(line_type, 'line.toml')

    # Return to directory containing corpus directory
    dir_up()

# For local testing
if __name__ == '__main__':
    create_corpus()
