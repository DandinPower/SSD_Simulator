a = [1, 2, 3, 4]
for b in a:
    b = 4

print(a)

a = [1, 2, 3, 4]
for i in range(len(a)):
    a[i] = 4

print(a)

class Variable:
    def __init__(self, value):
        self._value = value 
    
    def __repr__(self):
        return f'{self._value}'

a = [Variable(1), Variable(2), Variable(3), Variable(4)]

for b in a:
    b._value = 4 

print(a)

for i in range(len(a)):
    a[i]._value = 4

print(a)
