class Rule:

    def __init__(self,name,condition,conclusion):
        self.name = name[:-2]
        self.split_conditions(condition)
        self.extract_operation_and_conclusion(conclusion)

    def __str__(self):
        return "Meno: " + self.name + " \nAK (" + self.condition1 + self.condition2 + self.special_condition + ")\nPOTOM ((" + self.operation + " " + self.conclusion[1:] + ")\n"

    def split_conditions(self,full_condition):
        full_condition = full_condition[4:-2]
        first_end_index = full_condition.find(')')
        condition1 = full_condition[:first_end_index+1]
        full_condition = full_condition[first_end_index+1:]
        second_end_index = full_condition.find(')')
        condition2 = full_condition[:second_end_index+1]
        special_condition = full_condition[second_end_index+1:]

        self.condition1 = condition1
        self.condition1_variable_indexes = self.extract_variable_indexes(condition1)
        self.condition1_raw_text = self.extract_raw_condition_text(condition1)
        self.condition2 = condition2
        self.condition2_variable_indexes = self.extract_variable_indexes(condition2)
        self.condition2_raw_text = self.extract_raw_condition_text(condition2)
        self.special_condition = special_condition

    def extract_variable_indexes(self,condition):
        x = condition.find('?X')
        y = condition.find('?Y')
        z = condition.find('?Z')
        return {"X":x,"Y":y,"Z":z}


    def extract_raw_condition_text(self,condition):
        condition = condition.replace('?X','').replace('?Y','').replace('?Z','').replace('(','').replace(')','').replace('  ',' ')
        return condition

    def extract_operation_and_conclusion(self,conclusion):
        conclusion = conclusion[8:-2]
        first_space_index = conclusion.find(" ")
        operation = conclusion[:first_space_index]
        conclusion = "(" + conclusion[first_space_index+1:]
        self.operation = operation
        self.conclusion = conclusion