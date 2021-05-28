from selenium import webdriver
import bs4
import re



options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver_win32\chromedriver.exe", options=options)


def handle_fanfiction_story(url):
    if fanfiction_url_conts := re.search(r'm\.fanfiction\.net/([\s\S]+)', url):
        fanfiction_url_conts = fanfiction_url_conts.groups()[0]
        url = 'https://www.fanfiction.net/' + fanfiction_url_conts

    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')

    if soup.find('span', class_='gui_warning'):
        return -1

    try:
        if chaps := re.search(r'Chapters: (\d+)', soup.find('span', class_="xgray xcontrast_txt").text):
            num_of_chapters = chaps.groups()[0]
        else:
            num_of_chapters = 1  # one-shot

        chapter_num = re.search(r'https://www.fanfiction.net/s/\d+/(\d+)(?:/[\s\S]*)?', url).groups()[0]
        return int(num_of_chapters) > int(chapter_num)
    except AttributeError:  # if story is not found or no longer available
        raise Exception('ffn - wack')


def close_gracefully():
    driver.quit()


def handle_ao3_story(url):
    url = url.replace('#workskin', '')
    url = url.replace('#main', '')

    if "?view_adult=true" not in url: # to go through adult content warning
        url += "?view_adult=true"

    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')

    if soup.find('div', class_='system errors error-404 region'):
        return -1

    try:
        if chaps := re.search(r'(\d+)/(\d+)', (dd:=soup.find('dd', class_="chapters").text)):
            chapter_num, num_of_chapters = chaps.groups()
        elif chaps := re.search(r'(\d+)/\?', dd):
            num_of_chapters = chaps.groups()[0]
            print(soup.find('h3', class_="title").a.text)
            chapter_num = re.search(r'Chapter (\d+)', soup.find('h3', class_="title").a.text).groups()[0]
        else:
            raise Exception
        return int(num_of_chapters) > int(chapter_num)
    except:  # if story is not found or no longer available // probably need to change for Ao3 bc Ao3 could have a different setup than Fanfiction's
        raise Exception('ao3 - wack')


def handle_mangakakalot_story(url):
    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')

    num_of_chapters = re.search(r'Chapter (\d+(?:\.\d+)?)',
                                      soup.find('select', class_='navi-change-chapter').find('option').text).groups()[0]
    chapter_num = re.search(r'Chapter (\d+(?:\.\d+)?)', soup.find('h1', class_='current-chapter').text).groups()[0]

    return float(num_of_chapters) > float(chapter_num)

def handle_mangatx_story(url):
    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    if soup.find('section', class_='error-404 not-found'):
        return -1
    num_of_chapters = re.search(r'chapter-(\d+(?:\.\d+)?)', soup.find('select', class_='selectpicker single-chapter-select').findChildren('option')[
        -1]['value']).groups()[0]
    chapter_num = re.search(r'Chapter (\d+(?:\.\d+)?)', soup.find(id='chapter-heading').text).groups()[0]
    return float(num_of_chapters) > float(chapter_num)

def handle_mangasushi_story(url):
    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')


    # possibly
    # https://mangasushi.net/?s=just+by+living+there+i+become+the+strongest+in+the+world&post_type=wp-manga&op=&author=&artist=&release=&adult=
    # https://mangasushi.net/manga/my-house-is-a-magic-power-spot-just-by-living-there-i-become-the-strongest-in-the-world/chapter-54/
    # https://mangasushi.net/manga/ore-no-ie-ga-maryoku-spot-datta-ken-sundeiru-dake-de-sekai-saikyou/chapter-54/
    if soup.find('section', class_='error-404 not-found'):
        return -1

    num_of_chapters = re.search(r'chapter-(\d+(?:\.\d+)?)', soup.find('select', class_='selectpicker single-chapter-select').option['value']).groups()[0]
    chapter_num = re.search(r'Chapter (\d+(?:\.\d+)?)', soup.find(id='chapter-heading').text).groups()[0]

    return float(num_of_chapters) > float(chapter_num)

def handle_hiperdex_story(url):
    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    if soup.find('section', class_='error-404 not-found'):
        return -1
    num_of_chapters = soup.find('select', class_='selectpicker single-chapter-select').option['value'].replace('-','.')
    chapter_num = re.search(r'(\d+(?:\.\d+)?)', soup.find(id='chapter-heading').text).groups()[0]
    return float(num_of_chapters) > float(chapter_num)

def handle_readmanganato_story(url):
    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    if soup.find('section', class_='error-404 not-found'):
        return -1
    num_of_chapters = re.search(r'(\d+(?:\.\d+)?)', soup.find('select', class_='navi-change-chapter').option.text).groups()[0]
    chapter_num = re.search(r'chapter-(\d+(?:\.\d+)?)',url).groups()[0]
    return float(num_of_chapters) > float(chapter_num)

def handle_isekaiscan_story(url):
    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    if soup.find('section', class_='error-404 not-found'):
        return -1
    num_of_chapters = re.search(r'(\d+(?:\.\d+)?)', soup.find('select', class_='selectpicker single-chapter-select').option.text).groups()[0]
    chapter_num = re.search(r'chapter-(\d+(?:\.\d+)?)',url).groups()[0]
    return float(num_of_chapters) > float(chapter_num)

#
# print(handle_mangasushi_story('https://mangasushi.net/manga/ore-no-ie-ga-maryoku-spot-datta-ken-sundeiru-dake-de-sekai-saikyou/chapter-54/'))
# print(handle_mangasushi_story('https://mangasushi.net/manga/my-house-is-a-magic-power-spot-just-by-living-there-i-become-the-strongest-in-the-world/chapter-54/'))
# t = ['https://archiveofourown.org/series/2137872']
# # handle authors
# print(handle_ao3_story('https://archiveofourown.org/works/589726/chapters/6741035#workskin'))
# print(handle_mangatx_story('https://mangatx.com/manga/reverse-villain/chapter-48/'))
# print(handle_hiperdex_story('https://hiperdex.com/manga/the-wrong-way-to-use-healing-magic-en/034/'))
# print(handle_readmanganato_story('https://readmanganato.com/manga-gv983530/chapter-10'))
print(handle_isekaiscan_story('https://isekaiscan.com/manga/a-breakthrough-brought-by-forbidden-master-and-disciple/chapter-10/'))
