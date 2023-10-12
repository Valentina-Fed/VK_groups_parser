import requests
import pandas as pd
import datetime
import os

def parse_groups(groups):
    file = open(f'{groups}', 'r')
    group_id_list = ','.join([line.replace('ids: ', '') for line if line.startswith('ids') in file.readlines()])
    names_list = ','.join([line.replace('names: ', '') for line if line.startswith('names') in file.readlines()])
    return group_id_list, names_list

#to extract information from the wall
def main(path, groups):
    token = 'PUT YOUR ACCESS KEY HERE'
    version = '5.81'
    nb_posts = {}
    group_id_list, names_list = parse_groups(groups)
    max_likes = []
    for i,group_id in enumerate(group_id_list):
        wall = requests.get('https://api.vk.com/method/wall.get', params={'owner_id': group_id, 'access_token': token, 'v': version,
                                            'count':100})
        if 'response' in wall.json():
            nb_posts[names_list[i]] = wall.json()['response']['count']
        else:
            print(f'the group {names_list[i]} is not accessible')
            continue
        id, from_id, owner_id, date, post_type, post_text, attachments, post_source, likes, reposts, views = ([] for i in range(11))
        offset = 0
        while offset <= nb_posts[names_list[i]]:
            wall = requests.get('https://api.vk.com/method/wall.get',
                                params={'owner_id': group_id, 'access_token': token, 'v': version,
                                        'offset': offset, 'count': 100})
            text = wall.json()['response']['items']
            for tx in text:
                id.append(tx['id'])
                from_id.append(tx['from_id'])
                owner_id.append(tx['owner_id'])
                date.append(str(datetime.datetime.fromtimestamp(tx['date'])))
                post_type.append(tx['post_type'])
                post_text.append(tx['text'])
                if 'attachments' in tx.keys():
                    attachments.append(tx['attachments'][0]['type'])
                else:
                    attachments.append('no_information')
                post_source.append(tx['post_source']['type'])
                likes.append(tx['likes']['count'])
                if 'reposts' in tx.keys():
                    reposts.append(tx['reposts']['count'])
                else:
                    reposts.append('no_information')
                if 'views' in tx.keys():
                    views.append(tx['views']['count'])
                else:
                    views.append('no_information')
            offset += 100
        print(f'Processing the group {names_list[i]}')
        df = pd.DataFrame.from_dict({'id': id, 'text': post_text})
        df1 = pd.DataFrame.from_dict({'id': id, 'from_id': from_id, 'owner_id': owner_id, 'date': date, 'post_type': post_type, 'attachments': attachments,
              'post_source': post_source, 'likes': likes, 'reposts': reposts, 'views': views})
        df.to_csv(f'{path}{names_list[i]}_wall_text.csv', sep='\t', index=False)
        df1.to_csv(f'{path}{names_list[i]}_wall_info.csv', sep='\t', index=False)
        tfile = open(f'{path}{names_list[i]}_wall_text.txt', 'a')
        tfile.write(df.to_string())
        tfile.close()
        tfil = open(f'{path}{names_list[i]}_wall_info.txt', 'a')
        tfil.write(df1.to_string())
        tfil.close()
        id_max_likes = str(id[likes.index(max(likes))])
        max_likes.append(max(likes))
        print(f'Number of posts detected: {nb_posts}\nNumber of posts extracted: {len(id)}\nThe most popular post with id {id_max_likes} got {max_likes} likes')

#to extract information about group members
def users(path, groups):
    token = 'PUT HERE YOUR ACCESS KEY'
    version = '5.81'
    nb_members = {}
    group_id_list, names_list = parse_groups(groups)
    for i,group_id in enumerate(group_id_list):
        id, name, sex, city, country, bdate, university, schools = ([] for i in range(8))
        offset = 0
        members = requests.get('https://api.vk.com/method/groups.getMembers',
                               params={'group_id': group_id, 'access_token': token, 'v': version,
                                       'count': 1000})
        if 'response' in members.json():
            nb_members[names_list[i]] = members.json()['response']['count']
        else:
            print('the group ' + names_list[i] + ' is not accessible')
            continue
        while offset <= nb_members[names_list[i]]:
            members = requests.get('https://api.vk.com/method/groups.getMembers',
                                   params={'group_id': group_id, 'access_token': token, 'v': version,
                                           'fields': 'bdate, city, country, sex, schools, education, universities',
                                           'offset': offset, 'count': 1000})
            text = members.json()['response']['items']
            for tx in text:
                id.append(tx['id'])
                if 'first_name' in tx.keys() and 'last_name' in tx.keys():
                    name.append(f'{tx['first_name']} {tx['last_name']})
                else:
                    name.append('no_information')
                if 'sex' in tx.keys():
                    sex.append(tx['sex'])
                else:
                    sex.append('no_information')
                if 'city' in tx.keys():
                    city.append(tx['city']['title'])
                else:
                    city.append('no_information')
                if 'country' in tx.keys():
                    country.append(tx['country']['title'])
                else:
                    country.append('no_information')
                if 'bdate' in tx.keys():
                    bdate.append(tx['bdate'])
                else:
                    bdate.append('no_information')
                if 'universities' in tx.keys():
                    university.append([j['name'] for j in tx['universities']])
                else:
                    university.append('no_information')
                if 'schools' in tx.keys():
                    schools.append([j['name'] for j in tx['schools']])
                else:
                    schools.append('no_information')
            offset +=100
        print(f'Processing the group {names_list[i]}')
        df = pd.DataFrame.from_dict({'id': id, 'name': name, 'sex': sex, 'bdate': bdate, 'city': city,
              'country': country, 'universities': university, 'schools': schools})
        df.to_csv(f'{path}/{names_list[i]}_members.csv', sep='\t', index=False)
        tfile = open(f'{path}/{names_list[i]}_members.txt', 'a')
        tfile.write(df.to_string())
        tfile.close()

def compare_members (list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    if len(set1.intersection(set2)) > 0:
      return len(set1.intersection(set2))
    else:
      return 0

def common_members(list1, list2, file):
    set1 = set(list1)
    set2 = set(list2)
    if len(set1.intersection(set2)) > 0:
        return set1.intersection(set2)

def get_common_members(path, group):
    dico = {}
    df = pd.read_csv(f'{group}_members.csv', sep='\t')
    for file in os.listdir(path):
      if file.endswith('_members.csv'):
        file1 = file.replace('_members.csv', '')
        df1 = pd.read_csv(f'{file}', sep='\t')
        dico[file1] = compare_members(df1['id'], df['id'])
        if file1 != group:
            compare = common_members(df1['id'], df['id'], file)
            list_group = [df['name'][i] for i, value in enumerate(df['id']) if value in compare]
            tfile = open(f'{group}_common_members.txt', 'a')
            tfile.write(f'{group}\n{file1}: {', '.join(list_group)}\n\n')
            tfile.close()
    dico1 = sorted(dico.items(), key=lambda item: item[1], reverse=True)
    print(dico1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                      required=True,
                      help='path to directory where you would like to stock your data')
    parser.add_argument('--mode',
                      required=True,
                      help='choose between parsing the wall (--mode=wall) or members (--mode=members)')
    parser.add_argument('--groups',
                      required=False,
                      help='path to the txt-file with a list of group ids and group names')
    parser.add_argument('--group',
                      required=False,
                      help='path to the members.csv of the group to be compared with other groups')
    args = parser.parse_args()
    path = args.path
    groups = args.groups
    group = args.group
    mode = args.mode
    if mode == 'wall':
        main(path, groups)
    elif mode == 'members':
        if group:
            get_common_members(path, group)
        else:
            users(path, groups)





