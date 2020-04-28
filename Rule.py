class Rule:

    def __init__(self,name,condition,operation):
        self.name = name[:-2]
        self.condition = condition[:-1]
        self.operation = operation[:-1]

    def __str__(self):
        return self.name + ": \n" + self.condition + "\n" + self.operation + "\n"

    def get_name(self):
        return self.name
    def get_condition(self):
        return self.condition
    def get_operation(self):
        return self.operation