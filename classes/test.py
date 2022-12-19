class A:
    def a(self):
        print(1)


class B(A):
    def a(self):
        super().a()
        print(2)


t = B()
t.a()
