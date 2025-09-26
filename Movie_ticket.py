# Q6. Movie Ticket Pricing System
age = int(input("Enter Age: "))
movie_type = input("Enter Movie Type (2D/3D): ").lower()
day = input("Enter Day (weekday/weekend): ").lower()

price = 200
if movie_type == "3d":
    price += 100
if day == "weekend":
    price += 50

if age < 12:
    price *= 0.5
elif age > 60:
    price *= 0.7

print("Final Ticket Price =", price)
