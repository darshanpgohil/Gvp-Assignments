student = []

no = int(input("\n Enter The No Of Student : "))

i = 0

if no < 2:
    print("Give 3 Or More Student Only")
else:
    for i in range(no):
        name = input("Enter The student_name : ")
        sub1 = int(input("Enter The Subject1 Marks : "))
        sub2 = int(input("Enter The Subject2 Marks : "))
        sub3 = int(input("Enter The Subject3 Marks : "))
        sub4 = int(input("Enter The Subject4 Marks : "))
        sub5 = int(input("Enter The Subject5 Marks : "))

        total = sub1 + sub2 + sub3 + sub4 + sub5

        per = total / 5.0

        if per >= 90 and per <= 100:
             grade = 'A'
        elif per >= 80 and per < 90:
             grade = 'B'
        elif per >= 70 and per < 80:
             grade = 'C'
        elif per >= 60 and per < 70:
             grade = 'D'
        elif per >= 50 and per < 60:
             grade = 'E'
        elif per >= 41 and per < 50:
             grade = 'F'
        else:
             grade = 'Fail'

        # for i in range(no):
        #      i=i+1
        #      rank = i


        student.append([name,sub1,sub2,sub3,sub4,sub5,total,per,grade])

sorted =student.sort(key=lambda x:x[7],reverse=True)

for i in sorted:
     if i == 100.00:
          rank = rank+1
     elif i == i+1: 
          rank = rank
     else:
          rank = rank+1

print(f"{"Name":<10}{"Sub1":<10}{"Sub2":<10}{"Sub3":<10}{"Sub4":<10}{"Sub5":<10}{"Total":<10}{"Per":<10}{"Grade":<10}")

for student_reco in student:
        print(f"{student_reco[0]:<10} {student_reco[1]:<10} {student_reco[2]:<10} {student_reco[3]:<10} {student_reco[4]:<10} {student_reco[5]:<10} {student_reco[6]:<10} {student_reco[7]:<10} {student_reco[8]:<10}")