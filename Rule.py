class Conclusion:
    def __init__(self,whole_conclusion,operation,fact):
        self.whole_conclusion_text = whole_conclusion
        self.operation = operation
        self.fact = fact

class Rule:
    def __init__(self,name,condition,conclusion):
        self.name = name[:-2]
        self.full_condition_text = condition
        self.full_conclusion_text = conclusion
        self.conditions = self.split_conditions(condition)
        self.conclusions = self.split_conclusions(conclusion)
        self.full_rule_text = "Meno: " + self.name + "\n"  + condition + conclusion
        self.output_string = self.make_output_string()

    def __str__(self):
        return self.full_rule_text

    def make_output_string(self):
        result = self.name
        for c in self.conclusions:
            result += ', ' + c.whole_conclusion_text[1:-1]
        return result

    def split_conditions(self,full_condition):
        condition = full_condition[4:-2]
        conditions = []
        while condition != "":
            end_index = condition.find(')')
            current_condition = condition[:end_index+1]
            conditions.append(current_condition)
            condition = condition[end_index+1:]
        return conditions

    def split_conclusions(self,full_conclusion):
        conclusion = full_conclusion[7:-2]
        conclusions = []
        while conclusion != "":
            end_index = conclusion.find(')')
            current_conclusion = conclusion[:end_index + 1]
            current_operation,current_fact = self.extract_operation_and_fact(conclusion)
            conclusions.append(Conclusion(current_conclusion,current_operation,current_fact))
            conclusion = conclusion[end_index+1:]
        return conclusions

    def extract_operation_and_fact(self,conclusion):
        first_space_index = conclusion.find(" ")
        end_index = conclusion.find(")")
        operation = conclusion[1:first_space_index]
        fact = "(" + conclusion[first_space_index + 1 : end_index + 1]
        return operation, fact