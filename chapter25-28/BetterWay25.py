"""
super 로 부모 클래스를 초기화하자

클래스가 다중상속의 영향을 받는다면 슈퍼 클래스의 __init__ 메서드를 직접 호출하는 행위는
예기치 못한 동작을 일으킬 수 있다고 한다.

"""


class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class TimesTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


foo = OneWay(5)
print('foo : ', foo.value)
print('OneWay mro : ', OneWay.mro())


bar = AnotherWay(5)
print('bar : ', bar.value)
print('AnotherWay : ', AnotherWay.mro())

"""
MRO method resolution order
단일상속, 다중상속일 때 어느 순서로 메서드에 접근할지 __mro__에 순위가 매겨지는데
왼쪽에 있을수록 우선순위가 높다고 함.

여기서 문제는 OneWay 는 MRO 에 의거하여 생성자가 실행되지만, AnotherWay 는 MRO 에 상관없이.
부모클래스 생성자를 호출한 순서대로 생성자가 실행되기 때문에 문제라는 것이다.

또 다음 문제로는 다이아몬드 상속이 있다.
https://dojang.io/mod/page/view.php?id=2388
"""


class A(object):
    def __init__(self, value):
        self.value = value


class B(A):
    def __init__(self, value):
        A.__init__(self,value)
        self.value *= 5


class C(A):
    def __init__(self, value):
        A.__init__(self, value)
        self.value += 2


class D(B, C):
    def __init__(self, value):
        B.__init__(self, value)
        C.__init__(self, value)


foo = D(5)
print(foo.value)
print(D.mro())

"""
MRO 에 의하면 B의 생성자가 생기고 그 생성자를 C 클래스에서 +2 한 값 27 이 나와야 한다.
하지만 해당 생성자들이 호출되면 7이라는 값만 생성된다.

그 이유로는 B라는 클래스가 A라는 클래스를 호출하면 25라는 값이 생성될 것이다.
그후 C라는 클래스는 B의 생성자에 의해 생긴 25라는 값을 가지고 A를 호출하는게 아닌
초기에 입력받은 5라는 값으로 A 생성자를 호출하기때문에 최종적으로 남는 생성자 값은 7이된다.

이러한 문제들을 다이아몬드 상속 이라고 말한다.
"""


class A2(object):
    def __init__(self, value):
        self.value = value


class B2(A2):
    def __init__(self, value):
        super().__init__(value * 5)


class C2(A2):
    def __init__(self, value):
        super().__init__(value + 2)


class D2(B2, C2):
    def __init__(self, value):
        super().__init__(value)


foo = D2(5)
print(foo.value)
print(D.mro())

"""
MRO 는 어떤 슈퍼클래스 부터 초기화 하는지를 정한다 ( 깊이우선, 왼쪽에서 오른쪽 )
또한 다이아몬드 계층 구조에 있는 공통 슈퍼클래스를 단 한 번만 실행하게 된다.
"""