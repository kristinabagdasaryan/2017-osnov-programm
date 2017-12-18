import sys
import re
import string

result = []
readstates = []
word_dict = {}
nTokens = 0
POS_dict = {}
for state in text:
    readstates.append(json.loads(state))

for state in readstates:
    nTokens += len(state)
    for word in state:
        key = word[0] + '_' + word[2]
        if key in word_dict:
            word_dict[key] += 1
        else:
            word_dict[key] = 1

        if word[0] in POS_dict:
            POS_dict[word[0]] += 1
        else:
            POS_dict[word[0]] = 1


for token in word_dict:
    pos, wordform = token.split('_')
    count = word_dict[token]
    P = count/nTokens
    result.append([P, count, pos, wordform])

for pos in POS_dict:
    pos_count = POS_dict[pos]
    PPOS = pos_count/nTokens
    result.append([PPOS, pos_count, pos, '-'])

#print(word_dict)

for q in result:
    print(q)


