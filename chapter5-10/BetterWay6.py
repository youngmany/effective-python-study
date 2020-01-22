"""
한 슬라이스에 start, end, stride 를 함께 쓰지 말자
stride 는 간격이라는 의미로 N으로 지정을 했다면
슬라이스 할때 N번째 아이템들을 가져올 수 있다.
"""

from itertools import islice

a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = a[::2]  # red 에서 시작을 하여 짝수의 인덱스 요소들을 불러옴
evens = a[1::2]  # orange 부터 시작하여 2칸씩 띄우기 때문에 홀수의 인덱스 요소들을 불러옴
print(odds)  # ['red', 'yellow', 'blue']
print(evens)  # ['orange', 'green', 'purple']

"""
음수의 stride 는 피하는게 좋고
한 슬라이스에 파라미터 세 개를 사용해야 한다면 할당을 두번 하거나
내장 모듈 itertools 의 islice 를 사용하자.
islice(list, start, end, stride)
# https://docs.python.org/ko/3/library/itertools.html?highlight=islice#itertool-functions
"""

b = islice(a, 0, len(a)-1, 3)  # iterator
print('a islice 1 : ', next(b))  # a islice 1 :  red
print('a islice 2 : ', next(b))  # a islice 2 :  green

c = list(islice(a, 0, len(a)-1, 3))
for index, value in enumerate(c):
    print(index, '번째 islice value : ', value)
    #  0 번째 islice value :  red
    #  1 번째 islice value :  green
