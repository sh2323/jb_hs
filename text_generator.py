import random
from collections import Counter

file_name = input()
f = open(file_name, "r", encoding="utf-8")
words1 = f.read().split()
words = []
words_dict = {}


def gen_text(word1, word2, word_dict):
    line = list()
    rand_w = list()
    line.extend([word1, word2])
    prev = line[0]
    rand_w.append(line[1])
    count = 0
    ind = 2

    while count < 10:
        freq = Counter(word_dict[f'{prev} {rand_w[0]}']).most_common()
        weights = [freq[j][1] for j in range(len(freq))]
        population = [freq[j][0] for j in range(len(freq))]

        if ind < 2:
            prev = rand_w[0]
        else:
            prev = line[ind - 1]
        rand_w = random.choices(population, weights)

        if len(line) == 0 and (rand_w[0][-1] in '.!?' or not rand_w[0].istitle()):
            ind = 0
            continue
        line.append(*rand_w)
        ind += 1
        if len(line) >= 5 and line[-1][-1] in '.!?':
            print(*line)
            line.clear()
            count += 1
            ind = 0


for i in range(len(words1) - 2):
    words.append([words1[i], words1[i + 1], words1[i + 2]])

for key in words:
    words_dict.setdefault(f'{key[0]} {key[1]}', []).append(key[2])

random.seed()
rand_word = random.choice(words)

while True:
    if rand_word[0][-1] in '.!?' or rand_word[1][-1] in '.!?' or not rand_word[0].istitle():
        rand_word = random.choice(words)
    else:
        break

gen_text(rand_word[0], rand_word[1], words_dict)
