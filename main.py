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

def get_condition_string_pattern(condition):
    half_index = condition.find(")")
    condition1 = condition[4:half_index+1]
    condition2 = condition[half_index+1:-1]

    condition1 = condition1.replace("?X",".+")
    condition1 = condition1.replace("?Y", ".+")
    condition1 = condition1.replace("?Z", ".+")
    condition2 = condition2.replace("?X", ".+")
    condition2 = condition2.replace("?Y", ".+")
    condition2 = condition2.replace("?Z", ".+")
    return condition1,condition2



def resolve(facts,rule):
    condition1,condition2 = get_condition_string_pattern(rule.get_condition())
    for fact in facts:
        pattern = condition1
        if re.match(pattern, fact):
            print(fact)

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
