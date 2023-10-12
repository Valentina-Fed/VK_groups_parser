# -*- coding: utf-8 -*-
# pourcentage of reposts

import pandas as pd
import os

def nb_reposts(path):
  dico = {}
  for file in os.listdir(path):
    if file.endswith('wall_text.csv'):
      df = pd.read_csv(f'{file}', sep='\t')
      l = len(df['id'])
      df.dropna(subset = ['text'])
      file1 = file.replace('_wall_text.csv', '')
      dico[file1] = round(l/len(df['text']), 2)
  return dico

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory with wall_info.csv files')
    args = parser.parse_args()
    path = args.path
    nb_reposts(path)






