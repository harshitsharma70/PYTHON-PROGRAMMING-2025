# Q7. Online Examination Result
correct = int(input("Enter Correct Answers: "))
wrong = int(input("Enter Wrong Answers: "))
unattempted = int(input("Enter Unattempted Questions: "))

score = (correct * 4) + (wrong * -1)

if score >= 180:
    result = "Excellent"
elif score >= 120:
    result = "Good"
elif score >= 60:
    result = "Average"
else:
    result = "Fail"

print("Score =", score, "Result =", result)

if wrong > correct:
    print("Improve accuracy!")
