name = "Caroline "
print(name * 3)
print(name + "3")

"""
🧱🧱🧱
🧱🧱🧱
🧱🧱🧱
"""

def draw_square(size): 
    for i in range(size):
        # print ("🧱")
        for i in range (size):
            print("🧱", end ="")
        print()

""" 
Create a function to draw a triangle
🧱          1 = 0 + 1
🧱🧱        2 = 1 + 1
🧱🧱🧱      3 = 2 + 1
🧱🧱🧱🧱    4 = 3 + 1


In row im howmany bricks are there? i + 1 
"""
def draw_triangle(rows): 
    for i in range(rows): 
        print ("🧱" * (i + 1))


draw_triangle(4)

""" 
Draw a triangle like this (size = 5)

    #   0(i) 4 spaces + 1 # = 5    5 - 0 -1 = 4
   ##   1    3 spaces + 2 # = 5 `   5 - 1 -1 = 3
  ###   2     2 spaces + 3 # = 5    5 - 2 -1 = 2
 ####   3     1 space  + 4 # = 5    5 - 3 -1 = 1
#####   4     0 spaces + 5 # = 5    5 - 4 -1 = 0
"""

def draw_right_aligned_triangle(size):
    for i in range(size):
       print(" " * (size - i - 1) + "#" * (i + 1))
draw_right_aligned_triangle(5)