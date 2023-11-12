import os
import shutil
import uuid

from item import Item
from value import Value
from value_enum import VALUE, VARIABLE, FUNCTION


def random(length):
    return str(uuid.uuid4()).replace("-", "")[0:int(length)]


def aes(password, _key):
    return password + "-" + _key


def derive_key(factor1, factor2):
    return factor1 + "-" + factor2


def get_dependent_index(key, items):
    for item in items:
        value = item.value
        match_obj = ""
        if value.type == VARIABLE:
            match_obj = value.expression
        elif value.type == FUNCTION:
            match_obj = value.function_params
        if key in match_obj:
            return items.index(item)
    return -1


def sort_by_dependency(items):
    sorted_items = []
    for item in items:
        value = item.value
        if value.type != VALUE:
            continue
        sorted_items.append(item)
    for item in items:
        value = item.value
        if value.type == VALUE:
            continue
        dependent_index = get_dependent_index(item.key, sorted_items)
        if dependent_index != -1:
            sorted_items.insert(int(dependent_index), item)
        else:
            sorted_items.append(item)
    for index, item in enumerate(items):
        if item != sorted_items[index]:
            return False, sorted_items
    return True, sorted_items


def evaluate(sorted_items, _dict):
    for item in sorted_items:
        expression_value = eval(item.value.expression)
        _dict[item.key] = expression_value
        exec(item.key + " = '" + str(expression_value) + "'")


def write_dict_to_yaml(_dict, yaml_path):
    with open(yaml_path, "w") as f:
        for key, value in _dict.items():
            f.writelines(str(key) + ": " + str(value) + "\n")
        f.close()


if __name__ == '__main__':
    _dict = {}
    plain_dict = {}
    global_dict = {}
    items = []
    with open("global.yaml") as f:
        lines = f.readlines()
        for line in lines:
            key = line.split(":")[0].strip()
            value = line.split(":")[1].strip()
            item = Item(key, Value(value))
            items.append(item)
        f.close()
    completed, sorted_items = sort_by_dependency(items)
    while not completed:
        completed, sorted_items = sort_by_dependency(sorted_items)
    evaluate(sorted_items, _dict)
    for key, value in _dict.items():
        if "_plain" in key:
            plain_dict[key] = value
        else:
            global_dict[key] = value
    if os.path.exists("result"):
        shutil.rmtree("result")
    os.mkdir("result")
    write_dict_to_yaml(plain_dict, "result/plain.yaml")
    write_dict_to_yaml(global_dict, "result/global.yaml")
