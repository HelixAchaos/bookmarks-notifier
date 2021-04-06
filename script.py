import json
import os

from collections.abc import Iterable



possible_paths = [
    os.path.expanduser("~/.config/google-chrome/Default/Bookmarks"),
    os.path.expanduser(
        "~/Library/Application Support/Google/Chrome/Default/Bookmarks"),
    os.path.expanduser(
        "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks")
]

file_paths = [f for f in possible_paths if os.path.exists(f)]
if len(file_paths) == 0:
    print('wack, ya need to include the bookmarks path')
    exit(1)
elif len(file_paths) != 1:
    print('wth?')
    exit(2)

roots_nicks = {'Bookmarks bar': 'bookmark_bar', 'Other bookmarks': 'other', 'Mobile bookmarks': 'synced'}



def func(line: str) -> list[str]:
    for k, v in roots_nicks.items():
        line = line.replace(k, v)
    return line.split('/')


def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


with open('folders.txt', 'r') as folders_file:
    folder_list = [func(line) for line in folders_file.read().splitlines() if line]
    print(folder_list)

with open(file_paths[0], encoding="utf-8") as bookmarks_file:
    roots = json.load(bookmarks_file)["roots"]
    for folder_path in folder_list:
        temp = roots[folder_path[0]]
        for dir in folder_path[1:]:
            for child in temp['children']:
                if child['name'] == dir:
                    temp = child
                    break
            else:
                raise Exception(f'not found Error!\nfolder_path = {folder_path}\nchild = {child}')


        def get_children(dat: dict):
            if dat['type'] == 'url':
                return dat['url']
            else:
                return [get_children(chi) for chi in dat['children']]

        print(list(flatten(get_children(temp))))



