# Q5. University Admission System
phy = int(input("Enter Physics Marks: "))
chem = int(input("Enter Chemistry Marks: "))
math = int(input("Enter Math Marks: "))

total = phy + chem + math
avg = total / 3

if avg >= 70 and phy >= 60 and chem >= 60 and math >= 60:
    print("Eligible for Admission")
elif math >= 90:
    print("Eligible under Math Special Quota")
else:
    print("Not Eligible")
