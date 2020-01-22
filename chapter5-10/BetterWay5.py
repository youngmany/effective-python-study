"""
시퀀스를 슬라이스 하는 방법을 알자

슬라이싱 문법의 기본 형태는 somelist[start:end].
이때 start 는 포함, end 는 제외. 즉 start 부터 end-1까지 슬라이싱
"""

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('First 4: ', a[:4])  # ['a', 'b', 'c', 'd']
print('Last 4: ', a[-4:])  # ['e', 'f', 'g', 'h']
print('Middle two: ', a[3:-3])  # ['d', 'e']


"""
슬라이싱은 start 와 end 인덱스가 리스트의 경계를 벗어나도 적절하게 처리
하지만 슬라이싱이 아닌 경계를 벗어난 리스트에 접근하면 예외가 발생.
"""
first_twenty_items = a[:20]
print('first_twenty_items', first_twenty_items)  # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
last_twenty_items = a[-20:]
print('last_twenty_items', last_twenty_items)  # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# test = a[20]
"""
슬라이싱간 리스트의 인덱스를 음수로 할 경우 뜻밖의 결과를 얻는 상황이 발생할 수 있다.
인덱스가 -1 보다 작거나 같을경우는 상관없지만 -0이 될 경우가 존재한다
이 경우에는 원본 리스트를 복사한다.
"""

some_list = a[-0:]
print('some_list :', some_list)  # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

"""
슬라이싱 결과는 완전히 새로운 리스트이다.
슬라이싱간 할당 길이가 달라도 새로 들러온 값에 맞춰서 늘어나거나 줄어든다.
인덱스를 생략하고 슬라이스하면 원본의 복사본을 얻는다.
인덱스를 지정하지 않고 할당하면 슬라이스의 전채 내용을 참조 대상의 복사본으로 덮어쓴다.
"""

li = [1, 2, 3]
li = some_list[:]
print(li)  # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
