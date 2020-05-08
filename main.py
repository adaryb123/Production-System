from Rule import Rule

output_results = []

def load_facts():                       #load starting facts from facts.txt
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


def load_rules():                   #load rules from rules.txt
    print("Loading rules from rules.txt")
    file = open("rules.txt", "r")
    rules = []
    while True:
        name = file.readline()
        if name == "":
            break
        condition = file.readline()
        conclusion = file.readline()
        rules.append(Rule(name, condition, conclusion))
        file.readline()
    print("Rules loaded")
    return rules


def slice_string_to_next_space(string, start):          #extract first word from a string, useful for getting variables
    result = string[start:]
    space_index = result.find(' ')
    if space_index != -1:
        result = result[:space_index]
    other_index = result.find(')')
    if other_index != -1:
        result = result[:other_index]

    return result


def insert_variables_to_string(string, variables):      # replaces variables in string with actual values
    for key, value in variables.items():
        string = string.replace(key, value)
    return string


def execute_operation(conclusion_fact, operation,facts):        #executes possible operations : ADD(PRIDAJ), REMOVE(VYMAZ), SPRAVA(MESSAGE)
    if operation.upper() == "PRIDAJ":
        if facts.count(conclusion_fact) == 0:
            facts.append(conclusion_fact)
        else:
            return False,facts
    elif operation.upper() == "VYMAZ":
        if facts.count(conclusion_fact) == 0:
            return False,facts
        else:
            facts.remove(conclusion_fact)
    elif operation.upper() == "SPRAVA":
        print("\n\tSPRAVA: "+conclusion_fact[1:-1] + "\n")
    else:
        print("ERROR,unknown operation: " + operation)
        return False, facts
    return True, facts


def check_special_condition(pattern, variables):            # check if the special conditions is fulfilled. (values in variables are different)
    must_be_unique = []
    pattern = pattern[1:-1]
    while pattern != "":
        word = slice_string_to_next_space(pattern, 0)
        if word[0] == "?":
            must_be_unique.append(word)
        pattern = pattern[len(word) + 1:]

    are_unique = []
    for key in must_be_unique:
        value = variables[key]
        if are_unique.count(value) > 0:
            return False
        are_unique.append(variables[key])
    return True


def add_variables(variables, new):              #check if new values in variables match with previous ones , and add excess ones
    for key, value in new.items():
        if value != "":
            if variables.get(key) == value or variables.get(key) is None or variables[key] == "":
                continue
            else:
                return False, variables

    for key, value in new.items():
        if value != "":
            variables[key] = value

    return True, variables


def find_pattern_with_variables(pattern, fact):         # check if pattern from condition of rule matches pattern in fact string
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


def add_result(variables, rule):        #create Rule object with values instead of variables and add it to result array
    new_name = rule.name + ":\n"
    new_condition = insert_variables_to_string(rule.full_condition_text,variables)
    new_conclusion = insert_variables_to_string(rule.full_conclusion_text,variables)
    result = Rule(new_name,new_condition,new_conclusion)
    output_results.append(result)


def find_matching_fact(facts,rule,condition_index, variables):      # find matching facts for conditions in rule, with same variable values
    if condition_index >= len(rule.conditions):
        add_result(variables,rule)
        return

    pattern = rule.conditions[condition_index]

    if pattern.find("<>") != -1:
        if check_special_condition(pattern, variables):
            find_matching_fact(facts, rule, condition_index + 1, variables)
        else:
            return

    for fact in facts:
        pattern_found, current_variables = find_pattern_with_variables(pattern, fact)
        if pattern_found:
            variables_match, all_variables = add_variables(variables.copy(), current_variables)
            if variables_match:
                find_matching_fact(facts,rule, condition_index + 1, all_variables)


def one_step(facts,rules):          #execute first valid result from queue, and fill the result queue if its empty
    if len(output_results) == 0:
        for rule in rules:
            find_matching_fact(facts,rule,0,{})
    while True:
        if len(output_results) == 0:
            return True,facts       # no more results are found - program ends
        else:
            result = output_results.pop(0)
            invalid_result = False
            for conclusion in result.conclusions:
                execution_possible, facts = execute_operation(conclusion.fact, conclusion.operation, facts)
                if execution_possible == False:
                    invalid_result = True
                    break
            if invalid_result == False:
                print(result.output_string)
                return False,facts


facts = load_facts()
rules = load_rules()
while True:
    option = input("Enter 1 to make one step , Enter 2 to make all remaining steps, Enter 3 to print facts, Enter 4 to print rules: \n")
    if option == "1":
        is_end,facts = one_step(facts,rules)
        if is_end:
            print("FINISHED\n")
            print("Facts at the end:")
            for fact in facts:
                print("\t" + fact)
            exit(0)
    elif option == "2":
        while True:
            is_end, facts = one_step(facts, rules)
            if is_end:
                print("FINISHED\n")
                print("Facts at the end:")
                for fact in facts:
                    print("\t" + fact)
                exit(0)
    elif option == "3":
        for fact in facts:
            print(fact)
    elif option == "4":
        for rule in rules:
            print(rule)
    else:
        print("invalid input")
    print("____________________________________________________________________________________")
