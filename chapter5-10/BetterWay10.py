"""
range 보다는 enumerate 를 사용하자

종종 리스트를 순회하거나 리스트의 현재 아이템의 인덱스를 알고 싶은 경우가 있다.
예를 들어 아이스크림 리스트의 순위를 출력하고 싶다고 하자.

"""

flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s' % (i+1, flavor))
    # 1: vanilla
    # 2: chocolate
    # 3: pecan
    # 4: strawberry

"""
위의 코드는 리스트의 길이를 알아내야 하고, 배열을 인덱스로 접근해야 하며, 읽기 불편하다

파이썬은 이런 상황을 처리하려고 내장 함수 enumerate 를 제공한다.
이 제너레이터는 루프 인덱스와 다음 값을 한 쌍으로 가져와 넘겨준다.
* enumerate 두 번째 파라미터를 사용하면 인덱스 시작할 숫자를 지정할 수 있다. (기본값 0)
  또한 인덱스, 혹은 요소가 필요하지 않다면 _로 할당받지 않아도 된다
"""

for index, value in enumerate(flavor_list, 1):
    print('%d: %s ' % (index, value))

"""
코드의 간결함, 가독성을 책에서는 이유로 꼽고있지만 결론적으로는
구글링 해본 결과 iterator 인것과 아닌것의 차이인거 같다.
"""