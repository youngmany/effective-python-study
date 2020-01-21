'''
1. JSON 직렬화, 역직렬화 클래스 만들기
메타클래스를 사용하는 또 다른 일반적인 사례는 프로그램에 있는 타입을 자동으로 등록하는 것이다. 등록(Registration)은 간단한 식별자(Identifier)를 대응하는 클래스에 매핑하는 역방항 조회(Reverse lookup)를 수행할 때 유용하다.

예를 들어 파이썬 객체를 직렬화한 표현을 JSON으로 구현한다고 해보자. 객체를 얻어와서 JSON 문자열로 변환할 방법이 필요하다.

다음은 생성자 메소드의 인자를 저장하고 JSON 딕셔너리로 변환하는 기반 클래스를 범용적으로 정의한 것이다.
'''

import json

class Serializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})

# 직렬화된 데이터에 대응하는 타입(예를 들어 Point2D, BetterPoint2D)을 미리 알고 있을 때만 동작한다는 문제점이 있다. 그 이유는 역직렬화 함수가 특정 클래스에 바운딩되어 있기 때문이다.
class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

# point = Point2D(5, 3)
# print('Point     :', point)
# print('Serialized:', point.serialize())

class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

point = BetterPoint2D(7, 5)
print('Before    :', point)
data = point.serialize()
print('Serialized:', data)
after = BetterPoint2D.deserialize(data)
print('After     :', after)
