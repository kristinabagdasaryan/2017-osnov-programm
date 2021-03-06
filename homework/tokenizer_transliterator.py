import re
import sys 


row_tok_sents = []
tok_sents = [] 
let_dict = {'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'g',
            'д': 'd',
            'е': 'e',
            'ё': 'jo',
            'ж': 'zh',
            'з': 'z',
            'и': 'i',
            'й': 'i',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'kh',
            'ц': 'c',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'shch',
            'ъ': '″',
            'ы': 'y',
            'ь': '′',
            'э': 'e',
            'ю': 'ju',
            'я': 'ya'}

for c in sys.stdin.readlines():
    row_tok_sents.append(c.split())

for toksent in row_tok_sents:
    i = 1
    inxtoksent = []
    for word in toksent:
        transword = ''
        for letter in word:
            if letter.lower() in let_dict:
                transword += let_dict[letter.lower()]
            else:
                transword += letter
        inxtoksent.append([i, word, transword])
        i += 1
    tok_sents.append(inxtoksent)

t = 0
for q in tok_sents:
    if t < 100:
        print(q)
        t += len(q)
    else:
        break






