import threading
import logging
import os

from selenium import webdriver
from crawl_rank import crawl_rank
from todo_system import todo_queue, start_todo_queue, TodoItem

logging.basicConfig(level=logging.DEBUG)

os.environ['CONFIG_MODULE'] = 'config'

# 启动工作线程
todo_thread = threading.Thread(target=start_todo_queue, daemon=True)
todo_thread.start()

# 启动浏览器
driver = webdriver.Chrome()

# 开始爬取
start_url = 'https://www.photos18.com/sort/hits'

for page_num in range(1):
    if page_num > 0:
        new_start_url = f'{start_url}?page={page_num}'
    else:
        new_start_url = start_url

    todo_item = TodoItem(priority=-10, func=crawl_rank, args=[driver, new_start_url], kwargs={}, env={})
    todo_queue.put(todo_item)

todo_queue.join()
print('all job done')

driver.quit()
