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

def slice_string_to_next_space(string, start):
    result = string[start:]
    space_index = result.find(' ')
    if space_index != -1:
        result = result[:space_index]
    other_index = result.find(')')
    if other_index != -1:
        result = result[:other_index]

    return result


def insert_variables_to_string(string, variables):
    for key, value in variables.items():
        string = string.replace(key, value)
    return string

def execute_operation(string, operation):
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

def check_special_condition(pattern, variables):
    must_be_unique = []
    pattern = pattern[1:-1]
    while pattern != "":
        word = slice_string_to_next_space(pattern,0)
        if word[0] == "?":
            must_be_unique.append(word)
        pattern = pattern[len(word)+1:]

    are_unique = []
    for key in must_be_unique:
        value = variables[key]
        if are_unique.count(value) > 0:
            return False
        are_unique.append(variables[key])
    return True

def add_variables(variables, new):
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

def find_pattern_with_variables(pattern, fact):
    variables = {}
    pattern = pattern[1:-1]
    fact = fact[1:-1]
    while pattern != "":
        pattern_word = slice_string_to_next_space(pattern, 0)
        fact_word = slice_string_to_next_space(fact, 0)
        if pattern_word == fact_word:
            pattern = pattern[len(pattern_word) + 1:]
            fact = fact[len(fact_word) + 1:]
        elif pattern_word.find("?") != -1:
            pattern = pattern[len(pattern_word) + 1:]
            fact = fact[len(fact_word) + 1:]
            variables[pattern_word] = fact_word
        else:
            return False, {}
    return True, variables

def find_matching_fact(facts, conditions, condition_index, variables, conclusions):
    if condition_index >= len(conditions):
        for conclusion in conclusions:
            conclusion_with_variables = insert_variables_to_string(conclusion.fact,variables)
            execute_operation(conclusion_with_variables,conclusion.operation)
        return

    pattern = conditions[condition_index]

    if pattern.find("<>") != -1:
        if check_special_condition(pattern,variables):
            find_matching_fact(facts, conditions, condition_index+1, variables, conclusions)
        else:
            return

    for fact in facts:
        pattern_found, current_variables = find_pattern_with_variables(pattern, fact)
        if pattern_found:
            variables_match, all_variables = add_variables(variables.copy(), current_variables)
            if variables_match:
                find_matching_fact(facts, conditions, condition_index+1, all_variables, conclusions)

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
