class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def weight(self) -> int:
        return "84"

    def get_age(self,):
        return self.age

    def get_name(self,):
        return self.name

    def add_age(self, number: int):
        self.age = self.age + number
        return self.age


if __name__ == "__main__":
    p = Person("ken", 1)
    # tmp_dict = {'text':'1','int':1}
    p.add_age(p.weight)
    p.add_age(1)
    # p.add_age('1')
