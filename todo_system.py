import queue
import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)
todo_queue = queue.PriorityQueue()


@dataclass(order=True)
class TodoItem:
    priority: int # 优先级 数字越小越优先执行
    func: callable
    args: list
    kwargs: dict

    def __post_init__(self):
        if self.priority is None:
            self.priority = 0
        if self.args is None:
            self.args = list()
        if self.kwargs is None:
            self.kwargs = dict()


def start_todo_queue():
    while True:
        item = todo_queue.get()

        logger.info(f'Working on {item}')
        if item.func:
            item.func(*item.args, **item.kwargs)
        logger.info(f'Finished {item}')

        # 减速降低对网站压力
        time.sleep(3)
        todo_queue.task_done()
