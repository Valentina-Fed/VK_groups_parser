# -*- coding: utf-8 -*-
#pip install pyvis

from pyvis.network import Network
import os
import pandas as pd

def gender_sex_dob(file):
      df = pd.read_csv(f'{file}', sep='\t')
      return df['name'], df['sex'], df['bdate'], df['city'], df['country'], df['universities'], df['schools']

def main(path, limit):
  group_name = []
  names = {}
  for file in os.listdir('/content'):
    if file.endswith('members.csv'):
      df = pd.read_csv(f'{file}', sep='\t')
      filename = file.replace('_members.csv', '')
      for it in df['name']:
        names[it] = names.setdefault(it, 0) + 1
        tup = (filename, it)
        group_name.append(tup)
  group_names = []
  for pair in group_name:
    if names[pair[1]] > limit:
      group_names.append(pair)
  common_members = pd.DataFrame(group_names, columns =['group', 'name'])
  net = Network(notebook=True)

# Get a unique list of friends
  people = list(set(common_members.group).union(set(common_members.name)))

# Add nodes and edges
  net.add_nodes(people)
  net.add_edges(common_members.values.tolist())

  net.show("common_members.html")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory with wall_info.csv files')
    args = parser.parse_args()
    path = args.path
    main(path, 6)






