"""
믹스인 유틸리티 클래스에만 다중 상속을 사용하자

다중 상속으로 얻는 편리함과 캡슐화가 필요하다면 대신 믹스인을 작성하는 방안을 고려하자.
믹스인이란 클래스에서 제공해야 하는 추가적인 메서드만 정의하는 작은 클래스를 말한다.

동적 조사를 이용하면 많은 클래스에 적용할 수 있는 범용 기능을 믹스인에 한 번만 작성하면 된다.
믹스인들을 조합하고 계층으로 구성하면 반복 코드를 최소화하고 재사용성을 극대화할 수 있다.

"""


class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


tree = BinaryTree(10)
tree.left = BinaryTree(7, right=BinaryTree(9))
tree.right = BinaryTree(13, left=BinaryTree(11))
print(tree.to_dict())


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if isinstance(value, BinaryTreeWithParent) and key == 'parent':
            return value.value
        else:
            return super()._traverse(key, value)


root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())
# 순환에 빠지는 로직, root 생성후 root.left 에 parent 를 root 로 설정.
# root.left 가 생성된 후 parent 를 처리하려 root 에 접근을 하였더니 역시 left 를 가지고 있네?
# 그럼 root.left 를 처리 해볼까? 처리후 다시 parent 처리 하려 root 에 접근하였더니 또 left 가 있네?
# 무한 반복


class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent


my_tree = NamedSubTree('foobar', root.left.right)
print(my_tree.to_dict())

"""
믹스인을 조합할 수도 있다. 예를 들어 어떤 클래스에도 동작하는 범용 JSON 직렬화를 제공하는 믹스인이 필요하다고 해보자.
단, 이 믹스인은 클래스에 to_dict 메서드 (ToDictMixin 클래스에서 제공할 수도 있고 그렇지 않을 수도 있음) 가 있다고 가정
"""
import json
class JsonMixin(object):
    @classmethod
    # ClassMethod 를 사용하여 해당 클래스에 값 전달
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class DataCenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = switch
        self.machines = machines


serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 6, "ram": 32e9, "disk": 5e12},
        {"cores": 7, "ram": 32e9, "disk": 5e12}
    ]
}"""

deserialized = DataCenterRack.from_json(serialized)  # from_json 이 ClassMethod 이기 때문에 클래스를 첫번째 인자로 받음
roundtrip = deserialized.to_json()


print(json.loads(serialized))
print(json.loads(roundtrip))
assert json.loads(serialized) == json.loads(roundtrip)
