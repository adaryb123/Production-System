class Condition:
    def __init__(self,whole_condition,variable_indexes,raw_text):
        self.whole_condition_text = whole_condition
        self.variable_indexes = variable_indexes
        self.raw_text = raw_text

class Conclusion:
    def __init__(self,whole_conclusion,operation,fact):
        self.whole_conclusion_text = whole_conclusion
        self.operation = operation
        self.fact = fact


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
        self.split_conclusions(conclusion)
        self.full_rule_text = "Meno: " + self.name + "\n"  + condition + conclusion

    def __str__(self):
        return self.full_rule_text

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
            condition = condition.replace(variable_name,'_',1)
        #raw_text = condition.replace(')','').replace('(','').replace("  "," ")
        return variables,condition

    def split_conclusions(self,full_conclusion):
        conclusion = full_conclusion[7:-2]
        self.conclusions = []
        while conclusion != "":
            end_index = conclusion.find(')')
            current_conclusion = conclusion[:end_index + 1]
            current_operation,current_fact = self.extract_operation_and_fact(conclusion)
            self.conclusions.append(Conclusion(current_conclusion,current_operation,current_fact))
            conclusion = conclusion[end_index+1:]

    def extract_operation_and_fact(self,conclusion):
        first_space_index = conclusion.find(" ")
        end_index = conclusion.find(")")
        operation = conclusion[1:first_space_index]
        fact = "(" + conclusion[first_space_index + 1 : end_index + 1]
        return operation, fact