'''
실제로 메타클래스를 유용한 작업에 사용해보자. 앞서 이야기한 '클래스가 올바르게 정의됐는지 검증하는 작업'을 해볼 예정

명심: 다각형들의 기반이 되는 추상 다각형에는 검증을 적용하지 말아야 한다. 그 이유에는 일반적으로 추상 다각형에서는 속성에 None 과 같은 정의되지 않은 값을 설정하기 때문
'''

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases != ():
            if class_dict['sides'] < 3:
                raise ValueError("Polygon needs 3+ sides")

        return type.__new__(meta, name, bases, class_dict)

class AbstractPolygon(metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(AbstractPolygon):
    sides = 3

print('Start')
class Line(AbstractPolygon):
    print('Line class definition starts')
    sides = 1

    def test1(self):
        pass

    def test2(self):
        pass
    print('Line class definition ends')
print('Ended!')

# 에러가 출력되기 전 마지막 문장이 'Line 클래스 정의 종료'이다. 즉 클래스 선언의 다른 코드들이 다 실행된 후에 __new__ 메소드가 실행되는 것.
