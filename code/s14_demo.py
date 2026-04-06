a = [1, 2, 3]
b = a     # making an alias
b.append(4)
print(a)
print(a is b)

a = [1, 2, 3]
b = a[:]     # making a copy of the list
b.append(4)
print(a)
print(a is b)

