# -*- coding: utf-8 -*-
# pourcentage of reposts

import pandas as pd
import os

def isNaN(string):
    return string != string

def nb_reposts(path):
  dico = {}
  for file in os.listdir(path):
    count=0
    if file.endswith('wall_text.csv'):
      df = pd.read_csv(f'{file}', sep='\t').to_dict()
      l = len(df['id'].values())
      for text in df['text'].values():
        if isNaN(text) or text == '':
          count+=1
      file1 = file.replace('_wall_text.csv', '')
      dico[file1] = round(count/len(df['text'].values()), 2)
  print(dico)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory with wall_info.csv files')
    args = parser.parse_args()
    path = args.path
    nb_reposts(path)






