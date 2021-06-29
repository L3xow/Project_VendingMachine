

class TestClass:
    testnr = 5

    def __init__(self, c, d, e):
        self.a = 5
        self.b = 3
        self.c = c
        self.d = d
        self.e = e

    def calc(self):
        print(self.a + self.b + self.c + self.d)


class NewClass(TestClass):

    def __init__(self, a, b):
        super().__init__(a, b, 5)

    def calc(self):
        print(self.a + self.b + self.c + self.d)


def main():
    t = TestClass(5, 4, 3)
    t.calc()
    n = NewClass(3, 4)
    n.calc()

if __name__ == "__main__":
    main()
