# 메타클래스는 type 을 상속하여 정의하며, 자체의 __new__ 메소드에서 생성되고 있는 클래스의 정보를 여러 개 받는다. 

# type 클래스를 상속받고 자체의 __new__ 메소드를 구현하고 있다.
class Meta(type):
    # 클래스가 정의되기 전에 클래스의 모든 파라미터를 검증하려면 __new__에 기능을 추가
    def __new__(meta, name, bases, class_dict):
        print("  meta: ", meta) # meta: 메타클래스 자신을 말한다. 메소드에서 self, 클래스메소드에서 cls 를 지칭하는 것
        print("  name: ", name) # name: 클래스 자신의 이름
        print("  bases: ", bases) # bases: 클래스가 상속받은 부모클래스 여기서는 상속받지 않았기 때문에 빈 튜플
        print("  class_dict: ", class_dict) # 클래스가 가지게 될, 즉 clss.__dict__에 담기게 될 속성
        return type.__new__(meta, name, bases, class_dict)


# 다음은 Meta 를 메타클래스로 하는 MyClass 클래스를 정의했다. 메타클래스 선언은 클래스 이름 옆 () 괄호에 'metaclass' 인자로 지정한다. 이 클래스는 클래스 변수와 메소드 하나를 정의했다. 
class MyClass(metaclass=Meta):
    test  = 123

    def foo(self):
        pass
