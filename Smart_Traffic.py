# Q3. Smart Traffic Fine System
speed = int(input("Enter Vehicle Speed: "))
vehicle_type = input("Enter Vehicle Type (car/bike/truck): ").lower()
seat_belt = input("Wearing Seat Belt? (Yes/No): ").lower()
helmet = input("Wearing Helmet? (Yes/No): ").lower()

fine = 0

if speed > 80:
    fine += 2000
if vehicle_type == "car" and seat_belt == "no":
    fine += 1000
if vehicle_type == "bike" and helmet == "no":
    fine += 1500
if vehicle_type == "truck" and speed > 60:
    fine += 3000

if fine > 0:
    print("Total Fine =", fine)
else:
    print("No Fine. Drive Safe 🚗")
