"""
리스트 컴프리헨션에서 표현식을 두 개 넘게 쓰지 말자
"""

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]  # 표현식은 왼쪽에서 오른쪽 순서로 실행된다.
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

"""
위의 예제에서는 간단하고 읽기 쉽고 합당한 다중 루프를 사용했다고 한다
다중 루프의 또 다른 합당한 사용법은 입력 리스트의 레이아웃을 두 레벨로 중복해서 구성하는 것이다.
이 표현식은 추가로 [] 문자를 사용하기 때문에 좋아보이진 않지만 이해하기 쉽다고 한다

"""

squared = [[x**2 for x in row] for row in matrix]  # [] 를 사용하기 때문에 첫번째 [] 안에 있는 오른쪽부터 실행된다
print(squared)  # [[1, 4, 9], [16, 25, 36], [49, 64, 81]]

"""
하지만 3차원 배열식을 다른 루프에 넣는다면
리스트 컴프리헨션이 여러줄로 구분해야 할 정도로 길어진다
"""

my_lists = [
    [[1, 2, 3], [4, 5, 6]]
    #  ...
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]

"""
일반적인 루프문을 사용하면 여러줄의 컴프리헨션보다 이해하기가 쉽다
"""

flat2 = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat2.append(sublist2)

"""
리스트 컴프리헨션도 다중 if문 조건을 지원한다.
같은 루프 레벨에 여러조건이 있으면 암시적으로 and 표현식이 된다

하지만 좋은 방법은 아니다. 리스트 컴프리헨션을 사용하면 코드의 길이는 줄일 수 있지만
코드를 이해하기에는 매우 어렵기 때문이다. 

저자의 경험에 비추어 볼때 리스트 컴프리헨션을 사용할 때는 표현식이 두개 넘어가면 피하는게 좋다고 한다.
조건 두 개, 루프 두 개, 혹은 조건 한 개, 루프 한 개 정도가 적당하고 
이것보다 복잡해지면 일반적인 루프문 if, for 을 사용하고
헬퍼 함수를 작성해야 한다고 한다.
"""