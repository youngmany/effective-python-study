# 더는 생성자에 중복되는 이름 인자를 넘길 필요가 없다는 점이다. 대신 필드 디스크립터의 속성은 위의 Meta.__new__ 메소드에서 설정된다
class Field(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

# 중복성을 제거하려면 메타클래스를 사용하면 된다. 메타클래스를 이용하면 class 문을 직접 후킹하여 class 본문이 끝나자마자 원하는 동작을 처리할 수 있다.
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

# 다음은 메타클래스를 사용하는 기반 클래스를 정의한 코드다. 데이터베이스 레코드를 표현하는 클래스가 모두 이 클래스를 상속하게 해서 모두 메타클래스를 사용하게 해야 한다.
class DatabaseRow(metaclass=Meta):
    pass

class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

foo = BetterCustomer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'ymkim'
print('After :', repr(foo.first_name), foo.__dict__)

'''
메타클래스를 이용하면 클래스가 완전히 정의되기 전에 클래스 속성을 수정할 수 있다.
디스크립터와 메타클래스는 선언적 동작과 런타임 내부 조사(introspection)용으로 강력한 조합을 이룬다.
메타클래스와 디스크립터를 연계하여 사용하면 메모리 누수와 weakref 모듈 사용을 모두 피할 수 있다.
'''
