import PyPDF2
import os
import shutil
import re
import string
import wordninja
import gzip
import shutil

os.chdir('C:\\Users\\AlexZ\\Desktop\\CS410\\Project')

with open('testwords.txt', 'rb') as f_in:
    with gzip.open('testwords.txt.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

lm = wordninja.LanguageModel('testwords.txt.gz')

os.chdir('C:\\Users\\AlexZ\\Desktop\\CS410\\Project\\Data\\STAT 542 Slides\\Week_3')

def write_list(list, file_):
    with open(file_, 'w') as f:
        for l in list:
            f.write(l)
            f.write('\n')

lectures = os.listdir()

l = lectures[3]

file_reader = PyPDF2.PdfFileReader('AIC vs BIC.pdf')

raw = file_reader.getPage(0)

text = raw.extractText()

text = raw.extractText().encode("ascii", "ignore").decode()

text = re.sub('\s+', '', text)

# s_text = text.split()
# n_text = text.split()
#
# for word in s_text:
#     if len(word) > 40:
#         n_text.remove(word)
#
# text = ' '.join(n_text)

text = text.translate(str.maketrans('', '', string.punctuation))

print(text)

text = text.lower()

s_text = lm.split(text)
n_text = lm.split(text)

for word in s_text:
    if len(word) == 1:
        n_text.remove(word)

text = ' '.join(n_text)

pages = file_reader.getNumPages()
text_data = []
for page in range(0, pages):
    raw = file_reader.getPage(page)
    text = raw.extractText()
    text = raw.extractText().encode("ascii", "ignore").decode()
    text = re.sub('\s+', '', text)
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    text = text.lower()
    s_text = lm.split(text)
    n_text = lm.split(text)
    for word in s_text:
        if len(word) == 1:
            n_text.remove(word)
    text = ' '.join(n_text)
    text_data.append(text)

from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("testwords.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k
    return " ".join(reversed(out))
