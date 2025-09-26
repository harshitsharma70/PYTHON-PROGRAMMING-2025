# Q4. E-Commerce Discount Calculator
price = float(input("Enter Product Price: "))
user_type = input("Enter User Type (Regular/Premium/VIP): ").lower()
payment = input("Payment Mode (Online/Offline): ").lower()

discount = 0

if user_type == "regular":
    discount = 0.05 if price < 500 else 0.10
elif user_type == "premium":
    discount = 0.15 if price < 1000 else 0.20
elif user_type == "vip":
    discount = 0.25

if payment == "online":
    discount += 0.05

final_price = price * (1 - discount)
print("Final Discounted Price =", final_price)
