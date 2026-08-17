def student_data():
    student = []

    no = int(input("\n Enter The No Of Student : "))

    if no < 5:
        print("Give 5 Or More Student Only")
    else:
        for i in range(no):
            name = input("Enter The student_name : ")
            sub1 = int(input("Enter The Subject1 Marks : "))
            sub2 = int(input("Enter The Subject2 Marks : "))
            sub3 = int(input("Enter The Subject3 Marks : "))
            sub4 = int(input("Enter The Subject4 Marks : "))
            sub5 = int(input("Enter The Subject5 Marks : "))

    student.append([name,sub1,sub2,sub3,sub4,sub5])

    return student
        

def student_data_total(student):
    for i in student:
        if ((i[1] >=0 and i[1]<=100) and (i[2] >=0 and i[2]<=100) and (i[3]>=0 and i[3]<=100) and (i[4]>=0 and i[4]<=100) and (i[5]>=0 and i[5]<=100)):
            total = i[1] + i[2] + i[3] + i[4] + i[5]
            return total
        else:
            print("Invalid Marks! Please Enter Marks Between 0 And 100.")

    student.append(total)
    
    #         if sub1>40 and sub2>40 and sub3>40 and sub4>40 and sub5>40:
    #             per = total / 5.0

    #             if per >= 90 and per <= 100:
    #                 grade = 'A'
    #             elif per >= 80 and per < 90:
    #                 grade = 'B'
    #             elif per >= 70 and per < 80:
    #                 grade = 'C'
    #             elif per >= 60 and per < 70:
    #                 grade = 'D'
    #             elif per >= 50 and per < 60:
    #                 grade = 'E'
    #             elif per >= 41 and per < 50:
    #                 grade = 'F'
    #             else:
    #                 grade = 'Fail'
    #         else:
    #             grade = '-'
    #             per = 0.0