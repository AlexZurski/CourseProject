# bm25_master_eval.py scores a range of values for the BM25 ranking function.
# It retrieves the score from bm25_eval.py and returns the best score and
# the score's associated parameters

import bm25_eval

# Initialize values
best = 0
k1 = 0
b = 0

# For each k1 value
for i in range(1, 200, 1):

    # For each b value
    for j in range(1, 200, 1):

        # i and j are divided by 100 to test decimals

        # Run bm25_eval with chosen parameters
        new = bm25_eval.bm25_eval(i / 100, j / 100)

        # If the score is better than the previous best, replace parameters
        if new > best:
            k1 = i / 100
            b = j / 100
            best = new

# Print out best score and its associated parameters
# Could be better automated in the future
print(best)
print('k1 =' + str(k1) + ' ' + 'b = ' + str(b))
