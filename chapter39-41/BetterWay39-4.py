"""
Queue 클래스는 task_done 메서드로 작업 진행을 추적할 수도 있다. 작업 진행을 추적하면 특정 단계의 입력 큐가
빌 때 까지 기다릴 수 있으므로 파이프 라인의 끝에서 done_queue를 폴링하지 않아도 된다.
"""

from threading import Thread
from queue import Queue

in_queue = Queue(1)


def consumer():
    print('Consumer waiting')
    work = in_queue.get()
    print('Consumer working')
    print('Consumer done')
    in_queue.task_done()


Thread(target=consumer).start()
in_queue.put(object())
print('Producer waiting')
in_queue.join()
print('Producer done')

"""
이제 생산자는 조인으로 소비 스레드를 대기하거나 폴링을 하지 않아도 된다. 그냥 Queue 인스턴스의 join을 호출해서
in_queue가 완료하기를 기다리면 된다. 심지어 큐가 비더라도 in_queue의 join 메서드는 이미 큐에 추가된 모든 아이템에
task_done을 호출할 때까지 완료되지 않는다.
"""