class student:
    roll = 1
    name = "Darshan"

    def __init__(self,mark1,mark2):
        self.mark1 = mark1
        self.mark2 = mark2

    def student_total(self):
        return (self.mark1 + self.mark2)

    def student_data(self):
        total = self.student_total()
        return self.roll,self.name,total


student_info=student(100,100)

print(student_info.student_data())
# print(student_info.student_total())