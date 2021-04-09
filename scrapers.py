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
    try:
        if chaps := re.search(r'Chapters: (\d+)', soup.find('span', class_="xgray xcontrast_txt").text):
            num_of_chapters = chaps.groups()[0]
        else:
            num_of_chapters = 1  # one-shot

        chapter_num = re.search(r'https://www.fanfiction.net/s/\d+/(\d+)(?:/[\s\S]*){0,1}', url).groups()[0]
        return int(num_of_chapters) > int(chapter_num)
    except AttributeError:  # if story is not found or no longer available
        if soup.find('span', class_='gui_warning'):
            return -1
        else:
            raise Exception('wack')


def close_gracefully():
    driver.quit()


def handle_ao3_story(url):
    if fanfiction_url_conts := re.search(r'm\.fanfiction\.net/([\s\S]+)', url):
        fanfiction_url_conts = fanfiction_url_conts.groups()[0]
        url = 'https://www.fanfiction.net/' + fanfiction_url_conts

    driver.get(url)
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    try:
        if chaps := re.search(r'Chapters: (\d+)', soup.find('span', class_="xgray xcontrast_txt").text):
            num_of_chapters = chaps.groups()[0]
        else:
            num_of_chapters = 1  # one-shot

        chapter_num = re.search(r'https://www.fanfiction.net/s/\d+/(\d+)(?:/[\s\S]*){0,1}', url).groups()[0]
        return int(num_of_chapters) > int(chapter_num)
    except AttributeError:  # if story is not found or no longer available
        if soup.find('span', class_='gui_warning'):
            return -1
        else:
            raise Exception('wack')



t=['https://archiveofourown.org/works/29158347/chapters/71750658#workskin', 'https://archiveofourown.org/series/2137872']
# handle authors