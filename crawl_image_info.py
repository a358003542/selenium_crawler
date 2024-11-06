import logging
import time

from bs4 import BeautifulSoup

from download_image import download_image
from pywander.crawler.cache_utils import cachedb
from todo_system import TodoItem, todo_queue

logger = logging.getLogger(__name__)


def crawl_image_info(driver, new_url, **kwargs):
    result = []
    last_crawl = None

    if cachedb.get(new_url):
        page_source = cachedb.get(new_url)
    else:
        driver.get(new_url)
        driver.implicitly_wait(1)
        page_source = driver.page_source
        cachedb.set(new_url, page_source)
        last_crawl = time.time()

    soup = BeautifulSoup(page_source, 'html5lib')
    title = soup.title.get_text().strip()
    el_holder = soup.find_all(class_='imgHolder')

    for e_holder in el_holder:
        href = e_holder.a.get('href')

        result.append(href)

    for item in result:
        new_url = item
        logger.info(f'add: {new_url}')

        todo_item = TodoItem(priority=10, func=download_image, args=[new_url, title], kwargs={}, env={'last_crawl': last_crawl})
        todo_queue.put(todo_item)
