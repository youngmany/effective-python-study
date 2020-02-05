"""
파이프라인 정체 문제를 해결하려면 두 단계 사이에서 대기할 작업의 최대 개수를 Queue에 설정해야 한다.
큐가 이미 이 버퍼 크기만큼 가득 차 있으면 put 호출이 블록된다.
"""

from threading import Thread
from queue import Queue
import time

queue = Queue(1)


def consumer():
    time.sleep(0.1)
    queue.get()
    print('Consumer got 1')
    queue.get()
    print('Consumer got 2')


thread = Thread(target=consumer)
thread.start()

queue.put(object())
print('Product put 1')
queue.put(object())
print('Product put 2')
thread.join()
print('Producer done')

"""
대기 결과로 consumer 스레드에서 get을 호출하기 전에 생산 스레드에서 put으로 객체 두 개를 큐에 집어넣는 동작이
일어나야 한다. 하지만 Queue의 크기가 1이다. 다시 말해 두 번째 put 호출이 블록된 상태에서 빠져나와서
두 번째 아이템을 큐에 넣으려면 큐에 아이템을 추가하는 생산자는 소비 스레드에서 적어도 한 번은 get 호출하기를 기다려야한다.
"""