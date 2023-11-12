import re

from list_util import strip_string_list
from value_enum import FUNCTION, VARIABLE, VALUE

value_pattern = "(?<={{).+(?=}})"
params_pattern = "(?<=\()[^(,]+?(?=\))|(?<=,)[^(,]+?(?=\))|(?<=\()[^(,]+?(?=,)"


def get_pattern_value(pattern, _value):
    return str(re.findall(pattern, _value)[0]).strip()


def get_params(pattern, expression):
    return strip_string_list(re.findall(pattern, expression))


class Value:

    def __init__(self, content):
        self.content = content
        self.function_params = []
        if "{{" not in content:
            self.type = VALUE
            self.expression = content
            return
        self.expression = get_pattern_value(value_pattern, content)
        if "(" in self.expression:
            self.type = FUNCTION
            self.function_params = get_params(params_pattern, self.expression)
        else:
            self.type = VARIABLE
