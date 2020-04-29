from Rule import Rule
import re



def load_facts():
    print("loading facts from facts.txt")
    file = open("facts.txt", "r")
    facts = []
    while True:
        line = file.readline()
        if line == "":
            break
        facts.append(line[:-1])
    print("facts loaded")
    return facts

def load_rules():
    print("Loading rules from rules.txt")
    file = open("rules.txt","r")
    rules = []
    while True:
        name = file.readline()
        if name == "":
            break
        condition = file.readline()
        operation = file.readline()
        rules.append(Rule(name,condition,operation))
        file.readline()
    print("Rules loaded")
    return rules
"""
def get_condition_string_pattern(condition):
    condition = condition.replace("?X",".+")
    condition = condition.replace("?Y", ".+")
    condition = condition.replace("?Z", ".+")
    return condition
"""

def slice_string_to_next_space(string,start):
    result = string[start:]
    space_index = result.find(' ')
    if space_index != -1:
        result = result[:space_index]
    other_index = result.find(')')
    if other_index != -1:
        result = result[:other_index]

    return result

def assign_variables(fact,indexes):
    x = indexes["X"]
    y = indexes["Y"]
    z = indexes["Z"]

    lowest = -1
    middle = -1
    highest = -1

    raw_indexes = [x,y,z]
    for i in raw_indexes:
        if i == -1:
            raw_indexes.remove(i)

    print(raw_indexes)
    lowest = min(raw_indexes)
    raw_indexes.remove(lowest)
    if len(raw_indexes):
        middle = min(raw_indexes)
        raw_indexes.remove(middle)
        if len(raw_indexes):
            highest = raw_indexes[0]

    var_lowest = ""
    var_middle = ""
    var_highest = ""

    var_lowest = slice_string_to_next_space(fact,lowest)
    if middle != -1:
        var_middle = slice_string_to_next_space(fact,middle - 2 + len(var_lowest))
        if highest != -1:
            var_highest = slice_string_to_next_space(fact,highest - 4 + len(var_lowest) + len(var_middle))

    if indexes["X"] == lowest:
        var_x = var_lowest

    output = {}
    for key,value in indexes.items():
        if value == lowest:
            output[key] = var_lowest
        elif value == middle:
            output[key] = var_middle
        elif value == highest:
            output[key] = var_highest

    return output

def resolve(facts,rule):
    #print(rule.condition1_raw_text)
    #print(rule.condition2_raw_text)
    for fact in facts:
        pattern = rule.condition1_raw_text
        pattern_index = fact.find(pattern)
        if pattern_index != -1:

            output = assign_variables(fact,rule.condition1_variable_indexes)
            print(output["X"])
            print(output["Y"])
            print(output["Z"])
            """left_part = fact[1:pattern_index]
            right_part = fact[pattern_index+len(pattern):-1]
            print(left_part)
            print(right_part)"""


facts = load_facts()
rules = load_rules()

while True:
    available_rules = len(rules)
    for rule in rules:
        was_used, facts = resolve(facts,rule)
        if was_used == 0:
            available_rules -= 1

    if available_rules == 0:
        break

for fact in facts:
    print(fact)
