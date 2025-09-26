# Q9. Online Food Delivery Charges
distance = int(input("Enter Delivery Distance (km): "))
order_amount = float(input("Enter Order Amount: "))
user_type = input("Enter User Type (Normal/Gold/Platinum): ").lower()

# Delivery charges
delivery = 50
if distance > 5:
    delivery += (distance - 5) * 10
if order_amount >= 1000:
    delivery = 0

# Membership discount
discount = 0
if user_type == "gold":
    discount = 0.20
elif user_type == "platinum":
    discount = 0.30

order_amount -= order_amount * discount
final_bill = order_amount + delivery

print("Final Bill Amount =", final_bill)
