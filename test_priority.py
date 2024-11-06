import threading
import queue


todo_queue = queue.PriorityQueue()


def start_todo_queue():
    while True:
        item = todo_queue.get()
        if item[0] == 1:
            todo_queue.put((-5, 'new'))
        elif item[0] == 2:
            todo_queue.put((6, 'new2'))

        print(f'Working on {item}')
        print(f'Finished {item}')
        todo_queue.task_done()

# 启动工作线程
todo_thread = threading.Thread(target=start_todo_queue, daemon=True)
todo_thread.start()

def start_crawler():
    todo_queue.put((2, 'code'))
    todo_queue.put((1, 'eat'))
    todo_queue.put((3, 'sleep'))

start_crawler()

todo_queue.join()
print('all job done')

