# test_specs.py
"""Volume 1B: Testing.
<Name>
<Class>
<Date>
"""

import specs
import pytest

# Problem 1: Test the addition and fibonacci functions from specs.py
def test_addition():
    assert specs.addition(24, 13) == 37
    assert specs.addition(-52, 0) == -52
    assert specs.addition(2, 4) == 6
    assert specs.addition(120, 1020) == 1140

def test_smallest_factor():
    assert specs.smallest_factor(1) == 1
    assert specs.smallest_factor(2) == 2
    assert specs.smallest_factor(31) == 31
    assert specs.smallest_factor(91) == 7

# Problem 2: Test the operator function from specs.py
def test_operator():
    assert specs.operator(1, 2,'+') == 3
    assert specs.operator(12, -2,'+') == 10
    assert specs.operator(-1, 38,'+') == 37
    assert specs.operator(1, 2, '-') == -1
    assert specs.operator(9, 7, '-') == 2
    assert specs.operator(1, 2, '*') == 2
    assert specs.operator(17, -3, '*') == -51
    assert specs.operator(-4, -7, '*') == 28
    assert specs.operator(1, 2, '/') == 0.5
    assert specs.operator(20, 4, '/') == 5
    with pytest.raises(Exception) as excinfo:
        specs.operator(1, 0, '/')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "You can't divide by zero!"
    #pytest.raises(ValueError, specs.operator, a=1, b=0, oper='/')
    
    with pytest.raises(Exception) as excinfo:
        specs.operator(1, 2, '%')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper can only be: '+', '/', '-', or '*'"
    
    with pytest.raises(Exception) as excinfo:
        specs.operator(1, 2, '**')
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be one character"
    
    with pytest.raises(Exception) as excinfo:
        specs.operator(1, 2, 12)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Oper should be a string"
    
    #pytest.raises(ValueError, specs.operator, a=1, b=2, oper='%')
    #pytest.raises(ValueError, specs.operator, a=1, b=2, oper='**')
    #pytest.raises(ValueError, specs.operator, a=1, b=2, oper=12)
    

#problem 3 finish testing the complex number class
@pytest.fixture
def set_up_complex_nums():
    number_1 = specs.ComplexNumber(1, 2)
    number_2 = specs.ComplexNumber(5, 5)
    number_3 = specs.ComplexNumber(2, 9)
    return number_1, number_2, number_3

def test_complex_addition(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 + number_2 == specs.ComplexNumber(6, 7)
    assert number_1 + number_3 == specs.ComplexNumber(3, 11)
    assert number_2 + number_3 == specs.ComplexNumber(7, 14)
    assert number_3 + number_3 == specs.ComplexNumber(4, 18)

def test_complex_subtract(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 - number_2 == specs.ComplexNumber(-4, -3)
    assert number_1 - number_3 == specs.ComplexNumber(-1, -7)
    assert number_2 - number_3 == specs.ComplexNumber(3, -4)
    assert number_3 - number_3 == specs.ComplexNumber(0, 0)

def test_complex_multiplication(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 * number_2 == specs.ComplexNumber(-5, 15)
    assert number_1 * number_3 == specs.ComplexNumber(-16, 13)
    assert number_2 * number_3 == specs.ComplexNumber(-35, 55)
    assert number_3 * number_3 == specs.ComplexNumber(-77, 36)

def test_complex_conjugate(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1.conjugate() == specs.ComplexNumber(1, -2)
    assert number_2.conjugate() == specs.ComplexNumber(5, -5)
    assert number_3.conjugate() == specs.ComplexNumber(2, -9)

def test_complex_norm(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1.norm() == (1**2 + 2**2)**0.5
    assert number_2.norm() == (5**2 + 5**2)**0.5
    assert number_3.norm() == (2**2 + 9**2)**0.5

def test_complex_divide(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 / number_2 == specs.ComplexNumber(0.3, 0.1)
    assert number_1 / number_3 == specs.ComplexNumber(4.0/17, -1.0/17)
    assert number_2 / number_3 == specs.ComplexNumber(11.0/17, -7.0/17)
    assert number_3 / number_3 == specs.ComplexNumber(1, 0)

    with pytest.raises(Exception) as excinfo:
        number_1 / specs.ComplexNumber(0, 0)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "Cannot divide by zero"

def test_complex_eq(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 == specs.ComplexNumber(1, 2)
    assert number_2 == specs.ComplexNumber(5, 5)
    assert number_3 == specs.ComplexNumber(2, 9)

def test_complex_str(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert str(number_1) == '1+2i'
    assert str(number_2) == '5+5i'
    assert str(number_3) == '2+9i'

# Problem 4: Write test cases for the Set game.
def test_check_input():
    f1 = 'hands/set1.txt'
    f2 = 'hands/set2.txt'
    f3 = 'hands/set3.txt'
    f4 = 'hands/set4.txt'
    game1 = specs.get_file_contents(f1)
    game2 = specs.get_file_contents(f2)
    game3 = specs.get_file_contents(f3)
    game4 = specs.get_file_contents(f4)

    assert specs.check_input(game1) is None

    with pytest.raises(Exception) as excinfo:
        specs.check_input(game2)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == 'Incorrect number of cards in file.'
    
    with pytest.raises(Exception) as excinfo:
        specs.check_input(game3)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == 'Card has incorrect number of properties.'

    with pytest.raises(Exception) as excinfo:
        specs.check_input(game4)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == 'Card contains invalid attribute.'

def test_is_match():
    c1 = '0021'
    c2 = '0020'
    c3 = '1211'
    c4 = '2102'
    c5 = '0022'

    assert specs.is_match(c1, c2, c3) == False
    assert specs.is_match(c1, c3, c4) == False
    assert specs.is_match(c1, c2, c5) == True
    assert specs.is_match(c2, c3, c4) == True

def test_get_file_contents():
    f1 = 23
    f2 = 'not_a_real_file.txt'
    f3 = 'hands/set1.txt'
    
    game1 = ['0021', '0020', '1200', '2121', '1211', '2102', '2110', '1221', '0000', '1202', '2210', '0221']
 
    with pytest.raises(Exception) as excinfo:
        specs.get_file_contents(f1)
    assert excinfo.typename == 'TypeError'
    assert excinfo.value.args[0] == "Filename must be a string"

    with pytest.raises(Exception) as excinfo:
        specs.get_file_contents(f2)
    assert excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "File does not exist."

    assert specs.get_file_contents(f3) == game1

def test_set_finder():
    f1 = 'hands/set1.txt'

    assert specs.set_finder(f1) == 6

