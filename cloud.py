# -*- coding: utf-8 -*-
#!pip install pymorphy2
#!pip install wordcloud
#!pip install spacy

'''Create wordcloud from the wall of a group'''
import pymorphy2
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
import re
import os
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from spacy.lang.ru import Russian
nltk.download('punkt') # Loads a module required for tokenization
nlp = Russian()

morph = pymorphy2.MorphAnalyzer()

def lemmatize(text):
    words = list(itertools.chain(*[tx.split() for tx if type(tx) == str in text]))
    return [morph.parse(word)[0].normal_form for word in words]

stopw = ['её', 'd0', 'ли', 'том,',':', 'быть', 'тоже', 'около', 'чтоб', 'н', 'уж', '3gp', '8b', 'bd', 'b2', '3d', 'д', 'т', 'п', 'тем', 'между', 'пока', 'поэтому', 'про', 'среди', 'лишь', 'некоторый', 'и,', 'тогда', 'перед', 'ru', 'bb', 'd1', 'над','она','.', 'до','или', 'только', 'то', 'так', 'такой', 'ещё', 'тот', 'кто', 'же', 'самый', 'есть', 'уже', 'при', 'очень', 'где', 'когда', 'другой', 'также', 'более', 'чтобы', 'если', 'себя', 'даже', 'да', 'бы', 'под', 'каждый', 'после', 'https://vk.com/mp3/audio_api_unavailable.mp3', 'без', 'несколько', ',', 'г.', 'в.', 'вот', 'там', 'ни', 'того,', 'какой', 'через', 'нет', 'много', 'кроме', 'раз', 'чем', 'почти', 'всего', 'сам', '::', 'в','и','на','с', 'не', 'по', 'весь', 'что', 'из', 'это', '–', 'а', 'они', 'о','к', 'как', 'он', 'для', 'один', 'который', 'от', 'у', 'свой', 'за', '—','этот','но']
STOPWORDS.update(stopw)

def plot_cloud(text, file):
    wordcloud = WordCloud(width= 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(text)
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(f'{file}.png')

nlp.max_length = 4000000

def vocToStat(text):
    dico = {}
    for word in text.split(" "):
      if not re.match(r'\=+', word):
        dico[word] = dico.get(word, 0) + 1
    list_tuples = sorted(dico.items(), key=lambda x : x[1], reverse = True)[:500]
    return str(list_tuples).strip('[]')

def create_wordcloud(path):
    for file in os.listdir(path):
      if file.endswith('wall_text.csv'):
        df = pd.read_csv(f'{file}', sep='\t')
        text_lem = ' '.join(lemmatize(df['text']))
        phr = f'Словарь из 500 частотных слов из группы деревни {file}'
        dict_stat = vocToStat(text_lem)
        file2 = file.replace('_wall_text.csv', '')
        with open(f'{file2}.txt', 'w') as f:
          f.write(f'{phr}'\n'{dict_stat}')
        print(f'Printing wordcloud of the group {file2}')
        plot_cloud(text_lem, file)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory where you stock data')
    args = parser.parse_args()
    path = args.path
    create_wordcloud(path)
