# specs.py
"""Volume IB: Testing.
Tyler Moncur
1/10/2017
"""
import math
from itertools import combinations
import os.path

# Problem 1 Write unit tests for addition().
# Be sure to install pytest-cov in order to see your code coverage change.
def addition(a,b):
    return a + b

def smallest_factor(n):
    """Finds the smallest prime factor of a number.
    Assume n is a positive integer.
    """
    if n == 1:
        return 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i
    return n


# Problem 2 Write unit tests for operator().
def operator(a, b, oper):
    if type(oper) != str:
        raise ValueError("Oper should be a string")
    if len(oper) != 1:
        raise ValueError("Oper should be one character")
    if oper == "+":
        return a+b
    if oper == "/":
        if b == 0:
            raise ValueError("You can't divide by zero!")
        return a/float(b)
    if oper == "-":
        return a-b
    if oper == "*":
        return a*b
    else:
        raise ValueError("Oper can only be: '+', '/', '-', or '*'")

# Problem 3 Write unit test for this class.
class ComplexNumber(object):
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag

    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)

    def norm(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        return ComplexNumber(real, imag)

    def __sub__(self, other):
        real = self.real - other.real
        imag = self.imag - other.imag
        return ComplexNumber(real, imag)

    def __mul__(self, other):
        real = self.real*other.real - self.imag*other.imag
        imag = self.imag*other.real + other.imag*self.real
        return ComplexNumber(real, imag)

    def __div__(self, other):
        if other.real == 0 and other.imag == 0:
            raise ValueError("Cannot divide by zero")
        bottom = (other.conjugate()*other*1.).real
        top = self*other.conjugate()
        return ComplexNumber(top.real / bottom, top.imag / bottom)

    def __eq__(self, other):
        return self.imag == other.imag and self.real == other.real

    def __str__(self):
        return "{}{}{}i".format(self.real, '+' if self.imag >= 0 else '-',
                                                                abs(self.imag))

# Problem 5: Write code for the Set game here
def is_match(a, b, c):
    for i in range(4):
        if a[i] == b[i] == c[i]:
            continue
        if a[i] != b[i] != c[i] != a[i]:
            continue
        return False

    return True

def get_file_contents(filename):
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string")

    #check if file exists
    if not os.path.isfile(filename):
        raise ValueError("File does not exist.")
    
    with open(filename,'r') as target:
        lines = target.read().splitlines()
    target.close()

    return lines

def check_input(cards):
    if len(cards) != 12:
        raise ValueError('Incorrect number of cards in file.')

    for c in cards:
        if len(c) != 4:
            raise ValueError('Card has incorrect number of properties.')

    for c in cards:
        for i in c:
            if i not in '012':
                raise ValueError('Card contains invalid attribute.')

def set_finder(filename):
    cards = get_file_contents(filename)
    check_input(cards)

    count = 0
    for combo in combinations(cards, 3):
        if is_match(*combo):
            count += 1

    return count