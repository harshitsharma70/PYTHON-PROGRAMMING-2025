#Write a program to input the marks of 5 subjects and then calculate ● Total Marks Obtained ● Percentage of Marks ● Display grades

subject1 = float(input("Marks of 1st Subject:"))
subject2 = float(input("Marks of 2nd Subject:"))
subject3 = float(input("Marks of 3rd Subject:"))
subject4 = float(input("Marks of 4th Subject:"))
subject5 = float(input("Marks of 5th Subject:"))

total_marks = subject1 + subject2 + subject3 + subject4 + subject5

percentage = (total_marks/500) * 100

if percentage >= 90:
    grade = "A+"
elif percentage >= 80:
    grade = "A"
elif percentage >= 70:
    grade = "B"
elif percentage >= 60:
    grade = "C"
else:
    grade = "F"
    
print("Total Marks:",total_marks)
print("Percentage:",percentage,"%")
print("Grade:",grade)
     