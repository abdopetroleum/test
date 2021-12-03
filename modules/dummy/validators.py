from cerberus import Validator
from dataclasses import dataclass
import math, re
import numpy as np

@dataclass
class LinearEquation:
    eq: str
    
    def __init__(self, fields:dict = None):
        if fields is not None:
            for key in fields.keys():
                if key in fields.keys():
                    self.__setattr__(key, fields[key])
                    
@dataclass
class CalculationSet:
    operand1: float
    operand2: float
    method: str

    def __init__(self, fields:dict = None):
        if fields is not None:
            for key in fields.keys():
                if key in fields.keys():
                    self.__setattr__(key, fields[key])
                                        
@dataclass
class Coefficients:
    dividend_coefficients: list
    divisor_coefficients: list

    def __init__(self, fields:dict = None):
        if fields is not None:
            for key in fields.keys():
                if key in fields.keys():
                    self.__setattr__(key, fields[key])

class CoreValidator(Validator):

    def do_validation(self, obj):
        return self.validate(obj.__dict__)

    SOLVE_LINEAR_EQUATION_SCHEMA = {
        'equations': {
            'type': 'list',
            'schema': {'type': 'linear_equation'},
            'nullable': False,
        }
    }
    def _validate_type_linear_equation(self, value):
        """ Test for standard string equations.

        The rule's arguments are validated against this schema:
        {'type': 'string', 'nullable': False, 'linear equation': True,}

        :param field: field name.
        :param value: field value.
        """

        if re.match(r'^[0]*[1-9][\d]*[a-zA-Z][\s]*[+-][\s]*[0]*[1-9][\d]*[a-zA-Z][\s]*[=][\s]*[0]*[1-9][\d]*$', value, re.M|re.I):
            # self._error('Must be an standard equation. (like: "1x+2y=3" or "10x + 20y = 45")')
            return True
    
    CALCULATE_SCHEMA = {
        'operand1': {
            'type': 'float',
            'nullable': False,
        },
        'operand2': {
            'type': 'float',
            'nullable': False,
        },
        'method': {
            'type': 'string',
            'nullable': False,
        }
    }

    POLYNOMIAL_DIVISION_SCHEMA = {
        'dividend_coefficients': {
            'type': 'list',
            'schema': {'type': 'float'},
            'nullable': False,
        },
        'divisor_coefficients': {
            'type': 'list',
            'schema': {'type': 'float'},
            'nullable': False,
        }
    }


######################## Linear Equation, Validation example ##########################
# cv = CoreValidator(CoreValidator.SOLVE_LINEAR_EQUATION_SCHEMA)
# q = LinearEquation({
#     'equations': [ '1x + 1y = 7', '5x + 2y = 20', ],
# })
# print(cv.do_validation(q))
# print(cv.errors)
# print(cv.document)

######################## Calculation, Validation example ##########################
# cv = CoreValidator(CoreValidator.CALCULATE_SCHEMA)
# q = CalculationSet({
#     'operand1': 22,
#     'operand2': 3,
#     'method': '+',
# })
# print(cv.do_validation(q))
# print(cv.errors)
# print(cv.document)

######################## Polynomial Division, Validation example ##########################
# cv = CoreValidator(CoreValidator.POLYNOMIAL_DIVISION_SCHEMA)
# q = Coefficients({
#     'dividend_coefficients': [4, 9, 5, 4],
#     'divisor_coefficients': [1, 2],
# })
# print(cv.do_validation(q))
# print(cv.errors)
# print(cv.document)