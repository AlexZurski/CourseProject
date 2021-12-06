import bm25_eval

cfg = 'config.toml'

best = 0
k1 = 0
b = 0
k3 = 0

for i in range(1, 200, 1):
    for j in range(1, 200, 1):
        print(str(i) + ' ' + str(j))
        new = bm25_eval.bm25_eval(cfg, i / 100, j / 100)
        if new > best:
            k1 = i / 100
            b = j / 100
            best = new

print(best)
print(str(k1) + ' ' + str(b))
