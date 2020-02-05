"""
이런 모든 동작을 Queue의 서브클래스에 넣고, 처리를 중단해야 할 때 작업 스레드에 알리는 기능도 추가해보자.
다음은 close 메서드를 정의하여 더는 입력 아이템이 없음을 알리는 특별한 아이템을 큐에 추가하는 코드이다.
"""
from threading import Thread
from queue import Queue


def download(item):
    return item


def resize(item):
    return item


def upload(item):
    return item


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return  # Cause the thread to exit
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    # 스레드가 실제 실행하는 메서드
    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()
for _ in range(1000):
    download_queue.put(object())
download_queue.close()  # 현재 프로세스가 이 큐에 더는 데이터를 넣지 않을 것을 나타냅니다
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')
