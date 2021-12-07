# create_dict creates a dictionary with the key being the lecture number and the
# value being the lecture's name

import os
import shutil

# Move to the parent of the current directory
def dir_up():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

# Create dictionary of lecture names
def create_dict():

    # Change into directory containing each lecture's text data
    os.chdir('test_data')

    # Initialize empty dictionary
    course_dict = {}

    # Initialize lecture index at 0
    lec_num = 0

    # For each lecture
    for doc in os.listdir():

        # Update dictionary with lecture number and name
        course_dict.update({lec_num : doc})

        # Increment lecture number
        lec_num += 1

    # Move into directory containing text data directory
    dir_up()

    # Return the dictionary
    return(course_dict)

# For local testing
if __name__ == '__main__':
    create_dict()
