"""
1. this a sample to add two numbers or two strings together
2. to use docstring test the coding must be designed using a function
3. example

    def add(a,b)
        c = a + b
    return c

"""
"""
flowchart
"""
# this is my adding function

def add(a,b):
    """
    >>> add(2,3)
    10
    >>> add('a','b')
    'x'
    """

    c = a + b

    return c
# to run the program
if __name__ == "__main__":
    import doctest
    doctest.testmod()

"""
a = 5
b = 10

c = add(a,b)

print(c)

"""

