"""
진정한 병렬성을 실현하려면 concurrent.futures 를 고려하자

이 모듈을 이용하면 파이썬에서 자식프로세스로 추가적인 인터프리터를 실행하여 병렬로 여러 CPU 코어를 활용할 수 있다.
이런 자식 프로세스는 주 인터프리터와는 별개이므로 전역 인터프리터 잠금 역시 분리된다.
각 자식은 CPU 코어 하나를 완전히 활용할 수 있다. 또한 주 프로세스와 연결되어 계산할 명령어를 받고 수행한 결과를 반환한다.

예를 들어 파이썬으로 여러 CPU 코어를 활용해 계산 집약적인 작업을 한다고 하자.
두 숫자의 최대 공약수를 찾는 알고리즘을 구현해보자.
"""
import time
from concurrent.futures import ProcessPoolExecutor


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


numbers = [(1963309, 2265973), (2030677, 3814172), (15516545, 2229620), (2039045, 2020802)]
#start = time.time()
#results = list(map(gcd, numbers))
#end = time.time()
#print('%.3f' % (end-start))

"""
위의 코드는 병렬셩이 없으므로 순서대로 실행하면 시간이 선형적으로 증가한다.

이번에는 concurrent.futures 모듈의 ThreadPoolExecutor 클래스와 작업 스레드 두 개를 사용하여 동일한 계산을 수행해보자
"""
def main():
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, numbers))
    end = time.time()
    print('Took %.3f seconds' % (end - start))


if __name__ == '__main__':
    main()

"""
https://docs.python.org/dev/library/concurrent.futures.html#processpoolexecutor-example

The __main__ module must be importable by worker subprocesses. 
This means that ProcessPoolExecutor will not work in the interactive interpreter.

Calling Executor or Future methods from a callable submitted to a ProcessPoolExecutor will result in deadlock.
"""