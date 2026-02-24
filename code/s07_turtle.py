import turtle


def draw_square(turtle_obj, size = 100):
    """Draw a square with the given size."""
    for i in range(4):
        turtle_obj.forward(size)
        turtle_obj.left(90)

def draw_spiral(t): 
    """
    Draw one square, turn a angle, then draw another suare and so on""" 
    for i in range(72): 
        draw_square(t, 50 + i * 2)
        t.left(5)


