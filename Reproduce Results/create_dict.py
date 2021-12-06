# conda activate py36

import os
import shutil

def dir_up():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def create_dict():

    os.chdir('test_data')

    course_dict = {}
    lec_num = 0

    for doc in os.listdir():
        course_dict.update({lec_num : doc})
        lec_num += 1

    dir_up()

    return(course_dict)

if __name__ == '__main__':
    create_dict()
