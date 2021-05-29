import json
import os
import re
from collections.abc import Iterable

from scrapers import handle_fanfiction_story, close_gracefully, handle_ao3_story, handle_mangakakalot_story, handle_mangasushi_story, handle_mangatx_story, \
    handle_hiperdex_story, handle_readmanganato_story, handle_isekaiscan_story, handle_mangaclash_story, handle_nitroscans_story, handle_toonily_story, \
    handle_mangakik_story, handle_mangajar_story

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
    folder_list = [func(line) for line in folders_file.read().splitlines() if line and line[0] != '#']
    print(folder_list)

urls_list = []

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

    urls_list += list(flatten(get_children(temp)))



url_dict = {}
for url in urls_list:
    val = None
    print(url)

    if 'fanfiction.net/s/' in url:
        val = handle_fanfiction_story(url)
    elif "archiveofourown.org/works/" in url:
        val = handle_ao3_story(url)
    elif "mangakakalot.com/chapter/" in url:
        val = handle_mangakakalot_story(url)
    elif re.search(r'mangasushi.net/manga/[\s\S]+/chapter-', url):
        val = handle_mangasushi_story(url)
    elif re.search(r'mangatx.com/manga/[\w-]+/chapter-', url):
        val = handle_mangatx_story(url)
    elif re.search(r'hiperdex.com/manga/[\w-]+/\d+(?:-\d)?', url):
        val = handle_hiperdex_story(url)
    elif re.search(r'https://readmanganato.com/[\w-]+/chapter-', url):
        val = handle_readmanganato_story(url)
    elif re.search(r'https://isekaiscan.com/manga/[\w-]+/chapter-', url):
        val = handle_isekaiscan_story(url)
    elif re.search(r'https://mangaclash.com/manga/[\w-]+/chapter-', url):
        val = handle_mangaclash_story(url)
    elif re.search(r'https://nitroscans.com/manga/[\w-]+/chapter-', url):
        val = handle_nitroscans_story(url)
    elif re.search(r'https://toonily.net/manga/[\w-]+/chapter-', url):
        val = handle_toonily_story(url)
    elif re.search(r'https://mangakik.com/manga/[\w-]+/chapter-', url):
        val = handle_mangakik_story(url)
    elif re.search(r'https://mangajar.com/manga/[\w-]+/chapter/\d+(?:\.\d+)?', url):
        val = handle_mangajar_story(url)
    # if not(re.search(r'https://nitroscans.com/manga/[\w-]+/chapter-', url) or re.search(r'https://readmanganato.com/[\w-]+/chapter-', url) or re.search(
    #         r'https://mangaclash.com/manga/[\w-]+/chapter-', url) or re.search(
    #         r'https://isekaiscan.com/manga/[\w-]+/chapter-', url) or re.search(
    #         r'https://readmanganato.com/[\w-]+/chapter-', url) or re.search(
    #         r'hiperdex.com/manga/[\w-]+/\d+(?:-\d)?', url) or re.search(
    #         r'mangatx.com/manga/[\w-]+/chapter-', url) or 'fanfiction.net/s/' in url or
    #        "archiveofourown.org/works/" in url or
    # "mangakakalot.com/chapter/" in url or re.search(r'mangasushi.net/manga/[\s\S]+/chapter-', url)):
    #     print(url)

    url_dict[url] = val


print(url_dict)
print('\n'*10)
print([k for k,v in url_dict.items() if v is None])
close_gracefully()


dne_404 = ['https://www.pmscans.com/manga/leveling-up-by-only-eating/chapter-50/?style=list']
