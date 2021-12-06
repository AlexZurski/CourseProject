# conda activate py36

import PyPDF2
import os
import shutil
import time
import re
import string
import wordninja
import gzip

def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

def dir_up():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def write_txt(parent, child, file, name, course, week):
    os.chdir(parent)
    write_list(file, course + ' ' + week + ' ' + name + '.txt')
    os.chdir(child)

def create_bow():

    # # start timing
    # # for testing only
    # start = time.time()

    with open('qallwords.txt', 'rb') as f_in:
        with gzip.open('qallwords.txt.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    lm = wordninja.LanguageModel('qallwords.txt.gz')

    # Delete text_data if it already exists
    if ('test_data' in os.listdir()):
        shutil.rmtree('test_data')

    os.mkdir('test_data')
    os.chdir('test_data')
    parent = os.getcwd()

    dir_up()

    os.chdir('Data')

    classes = os.listdir()

    for course in classes:

        os.chdir(course)
        weeks = os.listdir()

        for week in weeks:

            os.chdir(week)
            child = os.getcwd()
            lectures = os.listdir()
            lectures = [lec for lec in lectures if lec.endswith(".pdf")]

            for lecture in lectures:

                text_data = []

                file_reader = PyPDF2.PdfFileReader(lecture)
                pages = file_reader.getNumPages()


                for page in range(0, pages):

                    #print(course + ' ' + week + ' ' + lecture + ' ' + str(page))

                    raw = file_reader.getPage(page)
                    text = raw.extractText()
                    text = text.encode("ascii", "ignore").decode()
                    text = re.sub('\s+', '', text)
                    text = text.lower()
                    text = text.translate(str.maketrans('', '', string.punctuation))
                    s_text = lm.split(text)
                    t_text = wordninja.split(text)
                    n_text = lm.split(text)
                    if len(t_text) < len(s_text):
                        s_text = wordninja.split(text)
                        n_text = wordninja.split(text)
                    for word in s_text:
                        if len(word) == 1:
                            n_text.remove(word)
                    text = ' '.join(n_text)
                    text_data.append(text)

                    #print('Done!')

                text_data = [' '.join(text_data)]
                write_txt(parent, child, text_data, lecture, course, week)



            dir_up()

        dir_up()

    dir_up()

    # # time how long this function takes
    # # for testing only
    # end = time.time()
    # print(end - start)


if __name__ == '__main__':
    # print('Creating queries')
    # create_query.py
    # print('Creating vocab')
    # create_vocab.py
    # print('Creating bag of words')
    create_bow()
