from Rule import Rule
import copy



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
    temp_dict = {}
    variable_names = {}
    result = {}

    for key,value in indexes.items():
        temp_dict[value] = ""

    bonus_lenght = 0
    while True:
        if len(temp_dict) == 0:
            break
        current = min(temp_dict.keys())
        temp_dict.pop(current)
        if current == -1:
            print("ERROR: -1")
        else:
            variable_string = slice_string_to_next_space(fact,current + bonus_lenght)
            variable_names[current] = variable_string
            bonus_lenght += len(variable_string)

    for key,value in indexes.items():
        result[key] = variable_names[value]

    return result

def create_conclusion_string(conclusion,variables):
    for key,value in variables.items():
        conclusion = conclusion.replace(key,value)
    return conclusion

#def execute_operation(facts,operation,conclusion):
#    if operation ==

def add_variables(variables,new):
    for key, value in new.items():
        if value != "":
            if variables.get(key) == value or variables.get(key) ==  None or variables[key] == "":
                continue
            else:
                return False,variables

    for key, value in new.items():
        if value != "":
            variables[key] = value

    return True, variables

def find_matching_fact(facts,conditions,condition_index,variables,conclusions):
    if condition_index >= len(conditions):
        for conclusion in conclusions:
            result = create_conclusion_string(conclusion.fact,variables)
            print(result)
        return

    pattern = conditions[condition_index].raw_text

    if pattern == "<> ":
        print("special condition-skip")
        find_matching_fact(facts,conditions,condition_index+1,variables,conclusions)

    for fact in facts:
        if fact.find(pattern) != -1:
            current_variables = assign_variables(fact,conditions[condition_index].variable_indexes)
            match, temp_variables = add_variables(variables.copy(), current_variables)
            if match:
                find_matching_fact(facts,conditions,condition_index+1,temp_variables,conclusions)

def resolve(facts,rule):
    index = 0
    find_matching_fact(facts,rule.conditions,index,{},rule.conclusions)
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
