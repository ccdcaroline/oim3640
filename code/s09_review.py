def mystery(x): 
    if x > 0: 
        return "positive"
    print("done")

result = mystery(5)
print(result)


x = 15 
y = x > 10 and x < 20 
print(type(y))
print(y)


def check(n):
    if n % 2 == 0:
        if n % 3 == 0:
            print("A")
        else:
            print("B")
    else:
        print("C")

check(8)
check(6)

