# -*- coding: utf-8 -*-

import collections
import matplotlib.pyplot as plt
import pandas as pd
import os


def gender_sex_dob(file):
      df = pd.read_csv(f'{file}', sep='\t').to_dict()
      return df['name'].values, df['sex'].values(), df['bdate'].values(), df['city'].values(), df['country'].values(), df['universities'].values(), df['schools'].values()


def gender(gender, file):
    g = {}
    print(gender)
    for s in gender:
      if s == 1 or s == 2:
        g[s]=g.setdefault(s, 0) + 1
    sex = (collections.OrderedDict(sorted(g.items()))).values()
    plt.figure(figsize = (8, 8))
    plt.pie(sex, labels = ['F', 'M'], colors = ['red', 'green'],
           autopct = lambda sex: str(round(sex, 2)) + '%')
    plt.legend()
    plt.savefig(f'{file}_gender.png',dpi=400)
    plt.show()


def bdate_plot(date, file):
    g = {}
    for s in date:
      if '.19' in str(s) or '.20' in str(s):
        if int(str(s)[len(str(s))-4:]) >= 2005:
          g['14-17']=g.setdefault('14-17', 0) + 1
        elif 1998 <= int(str(s)[len(str(s))-4:]) < 2005:
          g['18-24']=g.setdefault('18-24', 0) + 1
        elif 1993 <= int(str(s)[len(str(s))-4:]) < 1998:
          g['25-29']=g.setdefault('25-29', 0) + 1
        elif 1988 <= int(str(s)[len(str(s))-4:]) < 1993:
          g['30-34']=g.setdefault('30-34', 0) + 1
        elif 1983 <= int(str(s)[len(str(s))-4:]) < 1988:
          g['35-39']=g.setdefault('35-39', 0) + 1
        elif 1978 <= int(str(s)[len(str(s))-4:]) < 1983:
          g['40-44']=g.setdefault('40-44', 0) + 1
        elif 1973 <= int(str(s)[len(str(s))-4:]) < 1978:
          g['45-49']=g.setdefault('45-49', 0) + 1
        elif 1968 <= int(str(s)[len(str(s))-4:]) < 1973:
          g['50-54']=g.setdefault('50-54', 0) + 1
        elif 1963 <= int(str(s)[len(str(s))-4:]) < 1968:
          g['55-59']=g.setdefault('55-59', 0) + 1
        elif 1957 <= int(str(s)[len(str(s))-4:]) < 1963:
          g['60-65']=g.setdefault('60-65', 0) + 1
        elif int(str(s)[len(str(s))-4:]) < 1957:
          g['65+']=g.setdefault('65+', 0) + 1
      else:
        g['Не указано'] =g.setdefault('Не указано', 0) + 1
    plt.figure(figsize = (8, 8))
    cou = {}
    for k, v in sorted(g.items(), key=lambda item: item[0], reverse=True):
        cou[k] = v
    coun = list(cou.values())
    plt.pie(list(cou.values()), labels =  list(cou.keys()), 
            colors = ['red', 'yellow', 'green', 'blue', 'purple', 'violet', 'pink', 'orange'],
           explode = [0, 0, 0.2] + [0]*(len(coun)-3),
           autopct = lambda coun: str(round(coun, 2)) + '%',
           pctdistance = 0.7, labeldistance = 1.4)
    plt.legend()
    plt.savefig(f'{file}_bdate.png',dpi=400)
    plt.show()


def city_plot(city, file):
    g = {}
    for s in city:
        g[s]=g.setdefault(s, 0) + 1
    cou = {}
    for k, v in sorted(g.items(), key=lambda item: item[1], reverse=True):
      if '%%' not in str(k):
        cou[k] = v
      else:
        cou['Не указано'] =v
    coun = list(cou.values())
    plt.figure(figsize = (8, 8))
    plt.pie(coun[:10], labels =  list(cou.keys())[:10], 
            colors = ['red', 'yellow', 'green', 'blue', 'violet', 'pink', 'orange'],
           explode = [0, 0, 0.2] + [0]*7,
           autopct = lambda coun: str(round(coun, 2)) + '%',
           pctdistance = 0.7, labeldistance = 1.4)
    plt.legend()
    plt.savefig(f'{file}_city.png',dpi=400)
    plt.show()


def country_plot(country, file):
    g = {}
    for s in country:
        g[s]=g.setdefault(s, 0) + 1
    cou = {}
    for k, v in sorted(g.items(), key=lambda item: item[1], reverse=True):
      if '%%' not in str(k):
        cou[k] = v
      else:
        cou['Не указано'] =v
    coun = list(cou.values())
    plt.figure(figsize = (8, 8))
    plt.pie(coun[:3], labels = list(cou.keys())[:3], colors = ['red', 'yellow', 'green'],
           explode = [0, 0.2, 0],
           autopct = lambda coun: str(round(coun, 2)) + '%',
           pctdistance = 0.7, labeldistance = 1.4)
    plt.legend()
    plt.savefig(f'{file}_country.png',dpi=400)
    plt.show()


def main(path):
  for file in os.listdir(path):
    if file.endswith('members.csv'):
        name, sex, bdate, city, country, universities, schools = gender_sex_dob(file)
        gender(sex, file)
        city_plot(city, file)
        country_plot(country, file)
        bdate_plot(bdate, file)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory with members.csv files')
    args = parser.parse_args()
    path = args.path
    main(path)





