"""
공개 속성보다는 비공개 속성을 사용하자

파이썬에는 클래스 속성의 가시성이 공개(public)와 비공개(private) 두 유형밖에 없다.
"""

class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


foo = MyObject()
# 공개 속성은 어디서든 객체에 점 연산자를 사용하여 접근할 수 있다.
assert foo.public_field == 5
# 비공개 필드는 속성 이름 앞에 밑줄 두 개를 붙여 지정한다. 같은 클래스에 속한 메서드 에서는 비공개 필드에 접근 가능하다
assert foo.get_private_field() == 10
# 하지만 클래스 외부에서 직접 비공개 필드에 접근하면 예외가 발생한다.
#foo.__private_field  # 예외 발생


class MyOtherObject(object):
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field


bar = MyOtherObject()
# 클래스 메서드도 같은 class 블록에 선언되어 있으므로 비공개 속성에 접근 할 수 있다.
assert MyOtherObject.get_private_field_of_instance(bar) == 71

"""
비공개 필드라는 용어에서 예상할 수 있듯이 서브클래스에서는 부모 클래스의 비공개 필드에 접근할 수 없다.
"""

class MyParentObject(object):
    def __init__(self):
        self.__private_field = 71


class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field


baz = MyChildObject()
assert baz._MyParentObject__private_field == 71

"""
파이썬 컴파일러는 비공개 속성에 접근하는 코드를 발견하면 __private_field 를 _MyChildObject__private_field 에
접근하는 코드로 변환한다. __private_field 가  MyParentObject.__init__에 정의되어 있으므로 비공개 속성의 실제 이름은
_MyParentObject__private_field 가 된다.

즉 비공개 속성에 접근하는 동작은 단순히 변환된 속성 이름이 일치하지 않아서 실패한다.

객체의 속성 딕셔너리를 들여다보면 실제로 비공개 속성이 변환 후의 이름으로 저장되어 있음을 알 수 있다.
"""
print(baz.__dict__)  # {'_MyParentObject__private_field': 71}

"""
비공개 속성용 문법이 가시성을 엄격하게 강제하지 않는 이유는
"우리 모두 성인이라는 사실에 동의합니다" 라는 좌우명에 있다고 한다.

파이썬 프로그래머들은 개방으로 얻는 장점이 폐쇄로 얻는 단점보다 크다고 믿는다.

이외에도 속성에 접근하는 것처럼 언어 기능을 가로채는 기능( __getattr__, __getattribute__, __setattr__)이 있으면
마음만 먹으면 언제든지 객체의 내부를 조작할 수 있다.

파이썬 프로그래머들은 무분별하게 객체의 내부에 접근하는 위험을 최소화 하려고 스타일 가이드(PEP8)에 정의된 명명 관례를 따른다.
_protected_field 처럼 앞에 밑줄 한개를 붙인 필드는 보호필드로 취급해서 클래스의 외부 사용자들이 신중하게 다뤄야 함을 의미한다. 
하지만 파이썬을 처음 접하는 많은 프로그래머가 서브클래스나 외부에서 접근하면 안되는 내부 API를 비공개 필드로 나타낸다
"""

class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)


foo = MyClass(5)
assert foo.get_value() == '5'

"""
비공개 속성을 사용하면 서브클래스의 오버라이드와 확장을 다루기 어렵고 불안정할 뿐이다.
나중에 만들 서브클래스에서 꼭 필요하면 어전히 비공개 필드에 접근할 수 있다.
"""


class MyIntegerSubClass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)


foo = MyIntegerSubClass(5)
assert foo.get_value() == 5

"""
하지만 나중에 클래스의 계층이 변경되면 MyInterSubClass 같은 클래스는 비공개 참조가 더는
유효하지 않게 되어 제대로 동작하지 않을수 있다.

MyIntegerSubClass 클래스의 부모클래스인 MyClass에 MyBaseClass 라는 또 다른 부모 클래스를 추가했다고 하자

그리고 __value 속성을 MyClass 클래스가 아닌 MyBaseClass 에서 할당한다고 하면,
MyIntegerSubClass 에 있는 비공개 변수 참조는 동작하지 않는다.

self.MyClass__value 가 아닌 self.MyBaseClass_value 가 되기 때문이다.

결론적으로는 부모클래스의 비공개 변수를 참조하려면 _부모클래스명__비공개변수명으로 하드코딩이 되어야 하는데 
클래스 계층이 변경이 된다고 하면 해당된 하드코딩된 부분을 모두 고쳐줘야한다. 
이러한 부분이 유지보수에 큰 걸림돌이 된다는것 같다.

비공개 속성을 사용할지 진지하게 고민할 시점은 자식클래스와 이름이 충돌할 염려가 있을 때뿐이라고 한다.
이 문제는 자식클래스에서 부모클래스에 이미 정의된 속성을 정의할때 일어난다.
"""


class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'


a = Child()
print(a.get(), a._value)  # hello hello

"""
a.get()을 이용하여 Child 클래스의 부모 클래스인 ApiClass 의 _value 변수의 값을 가져와야 한다.
하지만 a 객체에도 _value 변수 값이 있기 때문에 부모클래스의 변수가 아닌 객체의 변수값을 가져온다.
즉 부모클래스의 변수와 자식클래스의 변수가 충돌한다.

이러한 상황이 일어날 위험을 줄이려면 부모클래스에서 비공개 속성을 사용해서 자식 클래스와
속성 이름이 겹치지 않게 하면 된다.
"""



