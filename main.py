from Rule import Rule

to_remove = []
to_add = []

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
            bonus_lenght += len(variable_string) - 1

    for key,value in indexes.items():
        result[key] = variable_names[value]

    return result

def insert_variables_to_string(string,variables):
    for key,value in variables.items():
        string = string.replace(key,value)
    return string

def execute_operation(string,operation):
    if operation.upper() == "PRIDAJ":
        to_add.append(string)
    elif operation.upper() == "VYMAZ":
        to_remove.append(string)
    elif operation.upper() == "SPRAVA":
        print(string[1:-1])
    elif operation.upper() == "OTAZKA":
        print("Otazka")
    else:
        print("ERROR,unknown operation: " + operation)

def check_special_condition(special,variables):
    unique = []
    for key,item in special.items():
        value = variables[key]
        if unique.count(value) > 0:
            return False
        unique.append(variables[key])
    return True

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

def find_pattern_in_string(pattern,string):
    while pattern != "":
        pattern_chunk = slice_string_to_next_space(pattern,0)
        string_chunk = slice_string_to_next_space(string,0)
        if pattern_chunk == string_chunk or pattern_chunk.find("_") != -1:
            pattern = pattern[len(pattern_chunk)+1:]
            string = string[len(string_chunk)+1:]
        else:
            return False
    return True

def find_matching_fact(facts,conditions,condition_index,variables,conclusions):
    if condition_index >= len(conditions):
        for conclusion in conclusions:
            conclusion_with_variables = insert_variables_to_string(conclusion.fact,variables)
            execute_operation(facts,conclusion_with_variables,conclusion.operation)
        return

    pattern = conditions[condition_index].raw_text

    if pattern == "(<> _ _)":
        if check_special_condition(conditions[condition_index].variable_indexes,variables):
            find_matching_fact(facts,conditions,condition_index+1,variables,conclusions)
        else:
            return

    for fact in facts:
        if find_pattern_in_string(pattern,fact):
            current_variables = assign_variables(fact,conditions[condition_index].variable_indexes)
            match, temp_variables = add_variables(variables.copy(), current_variables)
            if match:
                find_matching_fact(facts,conditions,condition_index+1,temp_variables,conclusions)

def resolve(facts,rule):
    index = 0
    find_matching_fact(facts,rule.conditions,index,{},rule.conclusions)
    for new_fact in to_add:
        if facts.count(new_fact) == 0:
            facts.append(new_fact)
    for old_fact in to_remove:
        facts.remove(old_fact)
    to_add.clear()
    to_remove.clear()
    return 0,facts

facts = load_facts()
rules = load_rules()
for rule in rules:
    print(rule)
    resolve(facts,rule)
    for fact in facts:
        print(fact)
    print("_______")
