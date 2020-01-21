'''
메타클래스로 구현할 수 있는 기능 중 하나는 클래스를 정의한 이후에, 하지만 실제로 사용하기 전에 프로퍼티를 수정하거나 주석을 붙이는 것이다. 보통 이 기법을 디스크립터와 함께 사용하여, 클래스에서 디스크립터를 어떻게 사용하는지 자세히 조사한 정보를 디스크립터에 제공한다.

예를 들어, 고객 데이터베이스의 로우를 표현하는 새 클래스를 정의한다고 하자. 테이블의 각 칼럼(Column)에 대응하는 클래스의 프로퍼티가 있어야 한다. 따라서 프로퍼티를 칼럼 이름과 연결하는 데 사용할 디스크립터 클래스를 다음과 같이 정의한다.
'''

class Field:
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# 문제는 Customer 클래스 정의에서 연산 순서가 왼쪽에서 오른쪽으로 읽는 방식과 반대라는 점이다. 먼저 Field 생성자는 Field('first_name') 형태로 호출한다. 다음 이 호출의 반환 값이 Customer.field_name 에 할당된다. 일반적인 변수 할당과 똑같다. 그러므로 Field에서는 자신이 어떤 클래스 속성에 할당될지 미리 알 방법이 없다.
class Customer:
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

foo = Customer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'ymkim'
print('After :', repr(foo.first_name), foo.__dict__)
