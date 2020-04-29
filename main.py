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
        conclusion = file.readline()
        rules.append(Rule(name,condition,conclusion))
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

def compare_variables(variables1,variables2):
    if variables1["X"] == variables2["X"] and variables1["X"] != "":
        return True
    elif variables1["Y"] == variables2["Y"] and variables1["Y"] != "":
        return True
    elif variables1["Z"] == variables2["Z"] and variables1["Z"] != "":
        return True
    return False

def combine_variables(variables1,variables2):
    output = {}
    for key,value in variables1.items():
        if value != "":
            output[key] = value

    for key,value in variables2.items():
        if value != "":
            output[key] = value

    return output

def create_conclusion_string(conclusion,variables):
    conclusion = conclusion.replace('?X',variables["X"])
    conclusion = conclusion.replace('?Y',variables["Y"])
    conclusion = conclusion.replace('?Z',variables["Z"])
    return conclusion

def execute_operation(facts,operation,conclusion):
    if operation ==

def resolve(facts,rule):

    for fact in facts:
        pattern = rule.condition1_raw_text
        if fact.find(pattern) != -1:
            condition1_variables = assign_variables(fact,rule.condition1_variable_indexes)
            for another_fact in facts:
                pattern = rule.condition2_raw_text
                if another_fact.find(pattern) != -1:
                    condition2_variables = assign_variables(another_fact, rule.condition2_variable_indexes)
                    if compare_variables(condition1_variables,condition2_variables):
                        variables = combine_variables(condition1_variables,condition2_variables)
                        conclusion = create_conclusion_string(rule.conclusion,variables)
                        #print(fact)
                        #print(another_fact)
                        #print(conclusion)
        #print("_____________________")
    return 0,facts

facts = load_facts()
rules = load_rules()
resolve(facts,rules[0])

"""while True:
    available_rules = len(rules)
    for rule in rules:
        was_used, facts = resolve(facts,rule)
        if was_used == 0:
            available_rules -= 1

    if available_rules == 0:
        break

for fact in facts:
    print(fact)"""
