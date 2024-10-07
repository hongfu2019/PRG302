import argparse
import doctest

def add(a, b):
    """
    Returns the sum of a and b.

    >>> add(2, 3)
    6
    >>> add(-1, 1)
    0
    """
    return a + b

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program or doctests.")
    parser.add_argument('--doctest', action='store_true', help="Run doctests")
    args = parser.parse_args()

    if args.doctest:
        doctest.testmod(verbose=True)
    else:
        # Normal program execution (replace with actual functionality)
        print("Run the program normally.")
