# create_bow.py converts pdf files into text data.
# The text data must be nested twice into directories with the heirarchy:
# Data (in the same directory as create_bow.py)
#    --> Courses
#            --> Weeks
#                   --> pdf files
# For each pdf file, the script looks at each page, extracts all text data into
# one contiunous string, removes punctuation, splits the continuous string into
# a list of words, deletes all one letter words, and then concatenates the list

import PyPDF2
import os
import shutil
import time
import re
import string
import wordninja
import gzip

# Write a list into a file with each element having a new line
def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

# Move to the parent of the current directory
def dir_up():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

# Write a list to a directory and then return to the original directory
# Text file name is 'course name' + 'week' + 'lecture name'
def write_txt(parent, child, file, name, course, week):
    os.chdir(parent)
    write_list(file, course + ' ' + week + ' ' + name + '.txt')
    os.chdir(child)

# Turn a dataset into their bag of words representation
def create_bow():

    # # start timing
    # # for testing only
    # start = time.time()

    # Gzip the list of words by frequency
    with open('qallwords.txt', 'rb') as f_in:
        with gzip.open('qallwords.txt.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Create a language model out of the above file
    lm = wordninja.LanguageModel('qallwords.txt.gz')

    # Delete text_data if it already exists
    # Less damaging solution to be looked for in the future
    if ('test_data' in os.listdir()):
        shutil.rmtree('test_data')

    # Create directory where all text files will be stored
    os.mkdir('test_data')
    os.chdir('test_data')

    # Assign the above directory to 'parent' for the write_txt function
    parent = os.getcwd()

    # Return to starting directory
    dir_up()

    # Move into data directory
    os.chdir('Data')

    # Retrieve all classes in the data directory
    classes = os.listdir()

    # For each class
    for course in classes:

        # Move into the course directory
        os.chdir(course)

        # Retrieve all weeks in the course directory
        weeks = os.listdir()

        # For each week
        for week in weeks:

            # Move into the week directory
            os.chdir(week)

            # Assign the week directory to 'child' for the write_txt function
            child = os.getcwd()

            # Retrieve all lectures in the week directory
            lectures = os.listdir()

            # Prune the list by only keeping pdf files
            # Only pdf files should be extracted, but just in case
            lectures = [lec for lec in lectures if lec.endswith(".pdf")]

            # For each lecture (pdf file)
            for lecture in lectures:

                # Initialize empty list
                text_data = []

                # Read file
                file_reader = PyPDF2.PdfFileReader(lecture)

                # Retrieve each page in the file
                pages = file_reader.getNumPages()

                # For each page
                for page in range(0, pages):

                    # Get the raw data from the page
                    raw = file_reader.getPage(page)

                    # Convert raw data into text data
                    text = raw.extractText()

                    # Change encode to ascii and ignore unknown symbols
                    # Ignoring symbols is necessary when dealing with equations
                    text = text.encode("ascii", "ignore").decode()

                    # Remove all spaces, new lines, etc.
                    text = re.sub('\s+', '', text)

                    # Convert all text into lowercase
                    text = text.lower()

                    # Remove all punctuation
                    text = text.translate(str.maketrans('', '', string.punctuation))

                    # Split the text data with the loaded language model
                    # Do it twice for pruning
                    s_text = lm.split(text)
                    n_text = lm.split(text)

                    # Split the text data with the default language model
                    # This is required as some documents don't split very well
                    # Needs to be debugged in the future
                    t_text = wordninja.split(text)

                    # When the spliiting fails, it splits the string letter by letter
                    # Therefore, the shorter of the two splits should be used
                    # May cause some issues in well split string, but the trade
                    # off is worth it
                    if len(t_text) < len(s_text):
                        s_text = wordninja.split(text)
                        n_text = wordninja.split(text)

                    # Prune the text by removing 1 letter words aka strings
                    # that are nonsense from equations, embeds, etc
                    for word in s_text:
                        if len(word) == 1:
                            n_text.remove(word)

                    # Rejoin list of words
                    text = ' '.join(n_text)

                    # Append single page's text data into lecture list
                    text_data.append(text)

                # After all pages are scraped, join the pages into one string
                text_data = [' '.join(text_data)]

                # Write string to a text file in text_data directory
                # and return to the week's directory
                write_txt(parent, child, text_data, lecture, course, week)

            # After all week's lectures are converted, return to directory of weeks
            dir_up()

        # After all weeks are converted, return to directory of courses
        dir_up()

    # After all courses are converted, return to original directory
    dir_up()

    # # time how long this function takes
    # # for testing only
    # end = time.time()
    # print(end - start)

# For local testing
if __name__ == '__main__':
    create_bow()
