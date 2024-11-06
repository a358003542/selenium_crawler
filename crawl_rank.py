import logging

from bs4 import BeautifulSoup
from crawl_image_info import crawl_image_info
from todo_system import TodoItem, todo_queue
from pywander.crawler.cache_utils import cachedb

logger = logging.getLogger(__name__)


def crawl_rank(driver, start_url):
    result = []

    netloc = 'https://www.photos18.com'

    if cachedb.get(start_url):
        page_source = cachedb.get(start_url)
    else:
        driver.get(start_url)
        driver.implicitly_wait(1)
        page_source = driver.page_source
        cachedb.set(start_url, page_source)

    soup = BeautifulSoup(page_source, 'html5lib')

    el_card = soup.find_all(class_='card')

    for e_card_item in el_card:
        e_card_a = e_card_item.find(class_='card-body')

        href = e_card_a.a.get('href')
        text = e_card_a.a.text
        item = {
            'href': href,
            'text': text
        }

        result.append(item)

    for item in result:
        new_url = netloc + item.get('href')
        logger.info(f'add: {new_url}')

        todo_item = TodoItem(priority=1, func=crawl_image_info, args=[driver, new_url], kwargs={})
        todo_queue.put(todo_item)
