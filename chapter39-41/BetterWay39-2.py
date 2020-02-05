"""
Queue로 문제 해결하기

내장모듈 queue에 들어 있는 Queue 클래스는 이런 문제를 해결하는데 필요한 기능을 모두 제공한다.
Queue는 새 데이터가 생길 때까지 get 메서드가 블록되게 하여 작업 스레드가 계속해서 데이터가 있는지
체크하는 상황을 없애준다.
"""
from threading import Thread
from queue import Queue
queue = Queue()


def consumer():
    print('Consumer waiting')  # 첫 번째로 출력
    queue.get()
    print('Consumer done')  # 세 번째로 출력


thread = Thread(target=consumer)
thread.start()

print('Product putting')  # 두 번째로 출력
queue.put(object())
thread.join()
print('Producer done')  # 네 번째로 출력
