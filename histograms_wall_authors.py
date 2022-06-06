# -*- coding: utf-8 -*-
'''Делаем гистограммы авторов постов'''
'''Create histograms and dictionnaries of authors of wall posts'''

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os


def plot(word_dict, file):
    hapax, pub = ([] for i in range(2))
    word_dict = dict(sorted(word_dict.items(), key=lambda item: item[1]))
    for k, v in word_dict.items():
        if v < 3:
            pub.append(k)
            hapax.append(k)
    for word in pub:
        word_dict.pop(word, None)
    x = np.arange(len(word_dict))
    palette = sns.color_palette("Paired", len(word_dict))
    plt.bar(x, list(word_dict.values()), color=palette)
    plt.xticks(x, list(word_dict.keys()), rotation=90)
    plt.figure(figsize=(8,10))
    plt.savefig(f'{file}_authors.png',dpi=400)


def authors_wall_posts(path):
    for file in os.listdir(path):
      if file.endswith('wall_info.csv'):
        df = pd.read_csv(f'{file}', sep='\t').to_dict()
        ids = df['from_id'].values()
        names={}
        for id in ids:
          names[id] = names.setdefault(id, 0) + 1
        file1 = file.replace('_wall_info.csv', '')
        df1 = pd.read_csv(f'{path}/{file1}_members.csv', sep='\t').to_dict()
        for_hist = {}
        id_list = list(df1['id'].values())
        name_list = list(df1['name'].values())
        for i, name in enumerate(id_list):
          for k,v in names.items():
            if name == k and v > 2:
              for_hist[name_list[i]] = v
            elif str(k).startswith('-'):
              for_hist['ADMIN'] = v
            elif v > 2:
              for_hist[k] = v
            else:
                continue
                plot(for_hist, file1)
        with open(f'all_authors.txt', 'w') as f:
          f.write(f'{file}' + '\n' + f'{sorted(for_hist.items(), key=lambda x : x[1], reverse = True)}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory with members.csv files')
    args = parser.parse_args()
    path = args.path
    authors_wall_posts(path)





