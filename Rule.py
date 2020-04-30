class Condition:
    def __init__(self,whole_condition,variable_indexes,raw_text):
        self.whole_condition_text = whole_condition
        self.variable_indexes = variable_indexes
        self.raw_text = raw_text


def slice_string_to_next_space(string, start):
   result = string[start:]
   space_index = result.find(' ')
   if space_index != -1:
        result = result[:space_index]
   other_index = result.find(')')
   if other_index != -1:
        result = result[:other_index]

   return result

class Rule:
    def __init__(self,name,condition,conclusion):
        self.name = name[:-2]
        self.split_conditions(condition)
        self.extract_operation_and_conclusion(conclusion)

    def __str__(self):
        return "Meno: " + self.name + " \nAK (" + self.condition1 + self.condition2 + self.special_condition + ")\nPOTOM ((" + self.operation + " " + self.conclusion[1:] + ")\n"

    def split_conditions(self,full_condition):
        condition = full_condition[4:-2]
        self.conditions = []
        while condition != "":
            end_index = condition.find(')')
            current_condition = condition[:end_index+1]
            current_variable_indexes,current_raw_text = self.extract_variable_indexes(current_condition)
            self.conditions.append(Condition(current_condition,current_variable_indexes,current_raw_text))
            condition = condition[end_index+1:]

    def extract_variable_indexes(self,condition):
        variables = {}
        while True:
            index = condition.find('?')
            if index == -1:
                break
            variable_name = slice_string_to_next_space(condition,index)
            variables[variable_name] = index
            condition = condition.replace(variable_name,'',1)
        raw_text = condition.replace(')','').replace('(','')
        return variables,raw_text

    def extract_operation_and_conclusion(self,conclusion):
        conclusion = conclusion[8:-2]
        first_space_index = conclusion.find(" ")
        operation = conclusion[:first_space_index]
        conclusion = "(" + conclusion[first_space_index+1:]
        self.operation = operation
        self.conclusion = conclusion