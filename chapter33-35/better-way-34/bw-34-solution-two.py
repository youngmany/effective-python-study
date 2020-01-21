'''
프로그래머가 의도한 대로 BetterSerializable 을 사용하고, 수동이 아닌 모든 경우에 register_class 가 호출된다고 확신하게 할 수는 없을까? 메타클래스를 이용하면 서브클래스가 정의될 때 class 문을 가로채는 방법으로 이렇게 만들 수 있다. 메타클래스로 클래스 본문이 끝나자마자 새 타입을 등록하면 된다.
'''
import json

registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class SerializeMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

# subclass 정의 시 register_class가 호출
class RegisteredSerializable(BetterSerializable, metaclass=SerializeMeta):
    pass

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vector 3D({self.x}, {self.y}, {self.z})'

v3 = Vector3D(10, -7, 100)
print('Before    :', v3)
data = v3.serialize()
print('Serialized:', data)
after = deserialize(data)
print('After     :', after)

'''
클래스 등록은 모듈 방식의 파이썬 프로그램을 만들 때 유용한 패턴이다.
메타클래스를 이용하면 프로그램에서 기반 클래스로 서브클래스를 만들 때마다 자동으로 등록 코드를 실행할 수 있다.
메타클래스를 이용해 클래스를 등록하면 등록 호출을 절대 빠뜨리지 않으므로 오류를 방지할 수 있다.
'''
