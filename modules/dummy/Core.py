from cerberus.errors import ValidationError
from .validators import CalculationSet, Coefficients, CoreValidator, LinearEquation
import numpy as np
import re
from utils import Exceptions

class Method:
    PLUS = '+'
    MINUS = '-'
    MULTIPY = '*'
    DEVIDE = '/'

def solve_linear_equations(equations:list):
    """Solving a System of Linear Equations like below...
    + function call:
    solve_linear_equations([ '1x + 1y = 7', '5x + 2y = 20', ])
    + result:
    [2, 5]

    :param equations: a list of equations as string
    :type equations: list

    :return: solution values
    :rtype: list
    """

    # validate inputs
    cv = CoreValidator(CoreValidator.SOLVE_LINEAR_EQUATION_SCHEMA)
    le = LinearEquation({
        'equations': equations
    })
    
    if not cv.do_validation(le):
        return cv.errors
    
    results = list()
    coefficients = list()
    
    for eq in equations:
        str_coefficients = re.findall(r'\d+', eq)
        results.append(float(str_coefficients.pop()))

        coefficient = list()
        for s in str_coefficients:
            coefficient.append(float(s))

        coefficients.append(coefficient)

    A = np.array([coefficients[0], coefficients[1]])
    B = np.array(results)
    solutions = np.linalg.solve(A,B)

    return [ round(f) for f in solutions ]

def calculate(operand1:float, method:str, operand2:float):
    """performs arithmetic operations on numbers like this:
    + function call:
    calculate(21, '-', 11)
    + result:
    10


    :param operand1: first operand to perform operation
    :type operand1: float
    :param method: operator
    :type method: str
    :param operand2: second operand to perform operation
    :type operand2: float

    :return: operation result
    :rtype: float
    """

    # validate inputs
    cv = CoreValidator(CoreValidator.CALCULATE_SCHEMA)
    cs = CalculationSet({
        'operand1': operand1,
        'operand2': operand2,
        'method': method,
    })
    
    if not cv.do_validation(cs):
        raise Exceptions.ValidationError('solve_linear_equations input validation failed', cv.errors)

    if method == Method.PLUS:
        return operand1 + operand2
    elif method == Method.MINUS:
        return operand1 - operand2
    elif method == Method.MULTIPY:
        return operand1 * operand2
    elif method == Method.DEVIDE:
        # if operand2 != 0:
        #     return operand1 / operand2
        # else:
        #     print('second operand must not be zero for {} operation'.format(method))
        return operand1 / operand2
    else:
        print('method was invalid')

def polynomial_division(dividend_coefficients:list, divisor_coefficients:list):
    """evaluates the division of two polynomials and returns the
    quotient and remainder of the polynomial division like below...
    + function call:
    polynomial_division([4, 9, 5, 4], [1, 2])

        [1, 2] repressented:
        1X + 2
        [4, 9, 5, 4] repressented:

        ..3....2....1
        
        4X + 9X + 5X + 4
    + result:

        qoutient:
          2    1
        4X + 1X + 3
        reminder:
        -2

    :param dividend_coefficients: [description]
    :type dividend_coefficients: list
    :param divisor_coefficients: [description]
    :type divisor_coefficients: list

    :return: polynomial of result quotient
    :rtype: str
    :return: polynomial of result reminder
    :rtype: str
    """

    cv = CoreValidator(CoreValidator.POLYNOMIAL_DIVISION_SCHEMA)
    c = Coefficients({
        'dividend_coefficients': dividend_coefficients,
        'divisor_coefficients': divisor_coefficients,
    })

    if not cv.do_validation(c):
        return cv.errors

    x = np.array(dividend_coefficients)
    y = np.array(divisor_coefficients)
    
    quotient, remainder = np.polydiv(x, y)

    return __coefficients_to_polynomials(quotient), __coefficients_to_polynomials(remainder)

def __coefficients_to_polynomials(coefficients:list, variable='X'):
    """get a list of coefficients and convert it to a polynomial as string

    :param coefficients: list of polynomials
    :type coefficients: list

    
    :return: result polynomial
    :rtype: str
    """
    polynomial = ''
    power = len(coefficients)-1
    for index, item in enumerate(coefficients):
        operator = ''
        if index+1 <= len(coefficients)-1:
            if coefficients[index+1] < 0:
                operator = '-'
            else:
                operator = '+'
        
        if item != 0:
            if power > 1:
                polynomial += str(__formatNumber(abs(item)))+str(variable)+'^'+str(power)+' {} '.format(operator)
            elif power == 1:
                polynomial += str(__formatNumber(abs(item)))+str(variable)+' {} '.format(operator)
            else:
                polynomial += str(__formatNumber(abs(item)))

        power -= 1

    return polynomial

def __formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num


######################## Linear Equation example ##########################
# soulutions = solve_linear_equations([ '1x + 1y = 7', '5x + 2y = 20', ])
# print(soulutions)

######################## Calculation example ##########################
# result = calculate(21, '*', 0)
# if result is not None:
#     print(result)   

######################## Polynomial Division example ##########################
# quotient, remainder = polynomial_division([10, 4, 9, 5, 4], [1, 2])
# print("quotient  : ", quotient)
# print("remainder : ", remainder)
