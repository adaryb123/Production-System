class Rule:

    def __init__(self,name,condition,operation):
        self.name = name[:-2]
        self.split_conditions(condition[4:-2])
        self.operation = operation[7:-2]

    def __str__(self):
        return "Meno: " + self.name + " \nAK (" + self.condition1 + self.condition2 + self.special_condition + ")\nPOTOM (" + self.operation + ")\n"

    def split_conditions(self,full_condition):
        first_end_index = full_condition.find(')')
        condition1 = full_condition[:first_end_index+1]
        full_condition = full_condition[first_end_index+1:]
        second_end_index = full_condition.find(')')
        condition2 = full_condition[:second_end_index+1]
        special_condition = full_condition[second_end_index+1:]

        self.condition1 = condition1
        self.condition1_variable_indexes = self.get_variable_indexes(condition1)
        self.condition1_raw_text = self.get_raw_text(condition1)
        self.condition2 = condition2
        self.condition2_variable_indexes = self.get_variable_indexes(condition2)
        self.condition2_raw_text = self.get_raw_text(condition2)
        self.special_condition = special_condition

    def get_variable_indexes(self,condition):
        x = condition.find('?X')
        y = condition.find('?Y')
        z = condition.find('?Z')
        return {"X":x,"Y":y,"Z":z}


    def get_raw_text(self,condition):
        condition = condition.replace('?X','').replace('?Y','').replace('?Z','').replace('(','').replace(')','').replace('  ',' ')
        return condition