# -*- coding: utf-8 -*-

'''Create histograms of wall publications per month, per year'''

import os
import collections
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_date(word_dict, name, file):
    x = np.arange(len(word_dict))
    palette = sns.color_palette("husl", len(word_dict))
    plt.bar(x, list(word_dict.values()), color=palette)
    plt.xticks(x, list(word_dict.keys()), rotation=90)
    plt.savefig(f'{file}_{name}.png',dpi=400)
    plt.show()


def print_hist(path):
    for file in os.listdir(path):
      if file.endswith('wall_info.csv'):
        df = pd.read_csv(f'{file}', sep='\t').to_dict()
        years = [date[:4] for date in df['date'].values()]
        months = [date[5:7] for date in df['date'].values()]
        print(f'Количество публикаций по годам в группе {file}\n')
        years_dict = {}
        for year in years:
          years_dict[year]=years_dict.setdefault(year, 0) + 1
        print(years_dict)
        plot_date(years_dict, 'years', file)
        print(f'Количество публикаций по месяцам в группе {file}\n')
        months_dict = {}
        for month in months:
          months_dict[month]=months_dict.setdefault(month, 0) + 1
        print(months_dict)
        plot_date(collections.OrderedDict(sorted(months_dict.items())), 'months', file)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory with wall_info.csv files')
    args = parser.parse_args()
    path = args.path
    print_hist(path)