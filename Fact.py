class Fact:

    def __init__(self,statement,object_identifier="?X"):
        objects_num = 0
        while True:
            object_index = statement.find(object_identifier)
            if object_index != -1:
                statement = statement[:object_index] + statement[object_index+len(object_identifier):]
            else:
                break
        self.objects_num = objects_num
        self.statement = statement

    def print_fact(self):
        print(self.object2 + self.statement + self.object1)

