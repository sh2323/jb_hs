import requests
import sys
from bs4 import BeautifulSoup

LANGUAGES = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
         'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

args = sys.argv


def reading_file(tran_word):
    file_r = open(f'{tran_word}.txt', 'r', encoding='utf-8')
    print(file_r.read(), end='')
    file_r.close()


def parsing(request, lan, tr_word):
    soup = BeautifulSoup(request.content, 'html.parser')
    words = soup.find_all('div', {"id": "translations-content"})
    sentences = soup.find_all('div', {'class': ['src', 'trg']})
    ans_words = []
    translate = open(f'{tr_word}.txt', 'a', encoding='utf-8')

    for w in words:
        ans_words += w.text.split('\n')

    ans_sents = [i.text.strip('\n ') for i in sentences if len(i.text.strip('\n ')) > 0]
    translate.write(f'{lan} Translations:\n')

    for el in ans_words:
        if len(el) > 0:
            translate.write(el.strip() + '\n')

    translate.write(f'\n{lan} Examples:\n')
    for i, el in enumerate(ans_sents):
        if i % 2 == 0:
            translate.write(el + '\n')
        elif i % 2 == 1:
            translate.write(el + '\n\n')
    translate.close()


lang_from = args[1]
lang_to = args[2]
word = args[3]
f = open(f'{word}.txt', 'w', encoding='utf-8')

if lang_to == 'all' and lang_from.title() in LANGUAGES:
    for index, ln in enumerate(LANGUAGES):
        if ln.lower() == lang_from:
            continue
        link = f'https://context.reverso.net/translation/{lang_from}-{LANGUAGES[index].lower()}/{word}'
        r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            parsing(r, LANGUAGES[index], word)
        elif str(r.status_code)[0] == 3:
            print('Something wrong with your internet connection')
        else:
            print(f'Sorry, unable to find {word}')
    reading_file(word)

elif lang_to.title() in LANGUAGES and lang_from.title() in LANGUAGES:
    link = f'https://context.reverso.net/translation/{lang_from}-{lang_to}/{word}'
    r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        parsing(r, lang_to.title(), word)
        reading_file(word)
    elif str(r.status_code)[0] == 3:
        print('Something wrong with your internet connection')
    else:
        print(f'Sorry, unable to find {word}')

else:
    if lang_from.title() in LANGUAGES:
        print(f"Sorry, the program doesn't support {lang_to}")
    else:
        print(f"Sorry, the program doesn't support {lang_from}")
