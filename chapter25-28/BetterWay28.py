"""
커스텀 컨테이너 타입은 collections.abc 의 클래스를 상속받게 만들자
"""


class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts


foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print(len(foo))  # 7
foo.pop()
print(type(repr(foo)))  # <class 'str'>
print(type(foo))  # <class '__main__.FrequencyList'>
print(foo.frequency())  # {'a': 3, 'b': 2, 'c': 1}

"""
list 의 서브클래스는 아니지만 인덱스로 접근할 수 있게 해서 list 처럼 보이는 객체를 제공하고 싶다고 해보자.
"""


class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


bar = [1, 2, 3]
print(bar[0])  # 1
print(bar.__getitem__(0))  # 1

"""
파이썬은 특별한 이름을 붙인 인스턴스 메서드로 컨테이너 동작을 구현한다.

bar[0] 같이 시퀀스의 아이템을 인데스로 접근하면 다음과 같이 해석된다고 한다.
bar.__getitem__(0)

그러므로 BinaryNode 클래스가 시퀀스처럼 동작하게 하려면 객체의 트리를 깊이 우선으로
탐색하는 __getitem__을 구현하면 된다.

*시퀀스?
순서가 있는 데이터 구조.
list tuple 등등
"""


class IndexAbleNode(BinaryNode):
    def _search(self, count, index):
        found = None
        if self.left:
            found, count = self.left._search(count, index)

        if not found and count == index:
            found = self
        else:
            count += 1

        if not found and self.right:
            found, count = self.right._search(count, index)
        return found, count

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError("Index out of range")
        return found.value


tree = IndexAbleNode(
    10,
    left=IndexAbleNode(
        5,
        left=IndexAbleNode(2),
        right=IndexAbleNode(
            6, right=IndexAbleNode(7)
        )
    ),
    right=IndexAbleNode(
        15, left=IndexAbleNode(11)
    )
)

print(tree.left.right.right.value)
print(tree[0])
print(tree[1])
# {'value': 10, 'left': <__main__.IndexAbleNode object at 0x0000018AC688D278>,
# 'right': <__main__.IndexAbleNode object at 0x0000018AC688D2E8>}
print(tree.__dict__)
print(11 in tree)
print(17 in tree)
print(list(tree))

"""
트리 탐색은 물론이고 list 처럼 접근할 수도 있다.

문제는 __getitem__을 구현하는 것만으로는 기대하는 시퀀스 시맨틱을 모두 제공하지 못한다는 점이다.
내장 함수 len을 쓰려면 커스텀 시퀀스 타입에 맞게 구현한 __len__ 이라는 또다른 특별한 메서드가 필요하다.
"""

class SequenceNode(IndexAbleNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count


"""
아직도 부족하다. 파이썬 프로그래머들이 list 나 tuple 같은 시퀀스 타입에서 기대할
count 와 index 메서드가 빠졌다. 커스텀 컨테이너 타입을 정의하는 일은 보기보다 어렵다.

파이썬에서는 이런 어려움을 피하려고 내장 collection.abc 모듈은 컨테이너 타입에 필요한
일반적인 메서드를 모두 제공하는 추상 기반 클래스들을 정의한다.

이 추상 기반 클래스들에서 상속받아 서브클래스를 만들다가 깜빡 잊고 필수 메서드를 구현하지 않으면
잘못되었다고 알려준다. ( 인터페이스 개념? )
"""

from collections.abc import Sequence

class BadType(Sequence):
    pass


foo = BadType()  # TypeError: Can't instantiate abstract class BadType with abstract methods __getitem__, __len__

"""
앞에서 다룬 SequenceNode 처럼 추상 기반 클래스가 요구하는 메서드(__getitem__, __len__)를 모두 구현하면
별도로 작업하지 않아도 index 와 count 같은 부가적인 메서드를 모두 제공한다

Set 와 MutableMapping 처럼 파이썬의 관례에 맞춰 구현해야하는 특별한 메서드가 많은 더 복잡한 타입을 정의할 때
이런 추상 기반 클래스를 사용하는 이점은 더욱 커진다.

ABC (Abstract Base Class) 추상화 클래스 ?
python 의 ABC 클래스는 Base 클래스를 상속받는 자식 클래스가 반드시 Base 클래스의 메서드를 명시적으로 선언해서
구현하도록 하는 강제하는 추상화 클래스이다.
https://bluese05.tistory.com/61
"""
