# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:35:39 2024

@author: hongf
"""

def add(a, b):
    """
    Adds two numbers together and returns the result.

    >>> add(2, 3)
    8
    >>> add('a', 'b')
    'x'
    
    """
    c = a+b
    return c

if __name__ == "__main__":
    import doctest
    doctest.testmod()
