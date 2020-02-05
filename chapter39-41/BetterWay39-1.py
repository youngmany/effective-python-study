"""
스레드 간의 작업을 조율하려면 Queue를 사용하자

많은 작업을 동시에 실행하는 파이썬 프로그램에서는 종종 작업들을 조율해 줘야한다.
가장 유용한 병행 작업 방식 중 하나는 함수의 파이프 라인이다.
이 방법은 파이썬으로 쉽게 병령화할 수 있는 블로킹 I/O나 서브 프로세스를 이용하는 작업에 특히 잘 맞는다.

디지털 카메라에서 끊임없이 이미지들을 가져와서 리사이즈하고 온라인 포토 갤러리에 추가하는 시스템을
구축한다고 하자. 이런 프로그램에서는 파이프라인을 세단계로 나눌수 있다.
이미지 추출 > 리사이즈 > 업로드

해당 작업을 동시에 처리하려면 파이프라인에 가장 먼저 필요한 것은 작업을 전달할 방법이다.
이 방법은 스레드 안전 생산자-소비자 큐(thread-safe producer-consumer queue)로 모델링 할 수 있다.
"""
from threading import Lock
from collections import deque
from threading import Thread
import time


def download(item):
    return item


def resize(item):
    return item


def upload(item):
    return item


class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    # 생산자인 디지털 카메라는 새 이미지를 대기 아이템 리스트의 끝에 추가한다.
    def put(self, item):
        with self.lock:
            self.items.append(item)

    # 소비자인 처리 파이프라인의 첫 번째 단계에서는 대기 아이템 리스트의 앞쪽에서 이미지를 꺼내온다.
    def get(self):
        with self.lock:
            return self.items.popleft()


"""
여기서는 이러한 큐에서 작업을 꺼내와서 함수를 실행한 후 결과를 또 다른 큐에 넣는 파이썬 스레드로 파이프라인의 각 단계를
표현한다. 또한 작업 스레드가 새 입력을 몇번이나 체크하고 작업을 얼마나 완료하는지 추적한다.
"""


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)  # No work to do
            except AttributeError:
                # The magic exit signal
                return
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


"""
가장 까다로운 부분은 이전 단계에서 아직 작업을 완료하지 않아서 입력 큐가 비어 있는 경우를 작업 스레드에서 적절하게
처리하는 것이다. run 함수 코드가 이에 해당한다.

이제 작업을 조율용 큐와 그에 해당하는 작업 스레드를 생성해서 세 단계를 연결하면 된다.
"""


download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

"""
스레드를 시작하고 파이프 라인의 첫 번째 단계에 많은 작업을 추가한다.
"""

for thread in threads:
    thread.start()
for _ in range(1000):
    download_queue.put(object())

while len(done_queue.items) < 1000:
    time.sleep(0.1)

for thread in threads:
    thread.in_queue = None

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling',
      polled, 'times')

"""
작업 수행 함수의 실행 속도가 제각각이면 초기 단계가 후속 단계의 진행을 막아 파이프라인이
정체될 수 있다. 그러면 후속 단계에서 처리할 것이 없어서 지속적으로 새 작업을 가져오려고
짧은 주기로 입력큐를 확인하게 된다.
결국 작업 스레드는 유용한 작업을 전혀 하지 않으면서 CPU 시간을 낭비한다

피해야할 문제가 3가지 더 있다.
입력 작업을 모두 완료했는지 판단하려면 done_queue에 결과가 모두 쌓일때까지 기다려야한다.
Worker의 run메서드는 루프에서 끊임없이 실행된다. 루프를 빠져나오도록 작업스레드에 신호를 줄 방법이 없다
최악의 문제로는 파이프라인이 정체되면 프로그램이 제멋대로 고장이 날 수 있다. 첫 번째 단계는 빠르게 진행하지만
두 번째 단계는 느리게 진행하면 첫 번째 단계와 두 번째 단계를 연결하는 큐의 크기가 계속 증가한다.
두번째 단계는 큐가 증가하는 속도를 따라잡지 못한다. 결국 메모리 부족으로 죽는다.

여기서 얻을 교훈은 파이프라인이 나쁘다는게 아니라 좋은 생산자-소비자 큐를 만들기 어렵다는 것이라고 한다.
"""