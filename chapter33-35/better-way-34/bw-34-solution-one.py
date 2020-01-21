# 클래스를 써야하는 복잡한 현실상황이라면 이상적으로는 JSON으로 직렬화되는 많은 클래스를 갖추고 그중 어떤 클래스든 대응하는 파이썬 객체로 역직렬화하는 공통 함수를 하나만 두려고 할 것이다.

# 이렇게 만들려면 직렬화할 객체의 클래스 이름을 JSON 데이터에 포함하면 된다.

import json

class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })
    
'''
    매핑을 관리할 dict 인 registry 와 여기에 클래스를 등록하는 함수와 역직렬화하는 함수를 register_class, deserialize 함수로 각각 만들었다. 이때 기억할 것은 이 변수와 함수들은 특정 클래스에 바운딩되어 있지 않은 글로벌 이름으로서, 다른 많은 서브클래스들에서 편하게 사용할 수 있다는 점이다.
'''
registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

# deserialize 가 항상 제대로 동작함을 보장하려면 추후에 역직렬화할 법한 모든 클래스에서 register_class 를 호출해야 한다.

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'EvenBetterPoint2D({self.x}, {self.y})'

register_class(EvenBetterPoint2D) # 클래스 등록!

point = EvenBetterPoint2D(5, 3)
print('Before:', point)

data = point.serialize()
print('Serialized: ', data)

after = deserialize(data)
print('After: ', after)
