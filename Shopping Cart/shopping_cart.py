'''
"Paws for Thoughts is a simple Python-based online pet food store application designed for efficiency 
and reliability. Utilising a user-friendly command-line interface, customers can easily explore 
a diverse range of pet supplies organised by pet type. The application features robust user management, 
allowing for secure account registration and cart storage, with data stored in separate .txt files. 
With strong error-handling mechanisms in place, the program ensures smooth operation and provides 
clear feedback.''' 

import json

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class ShoppingCart:
    def __init__(self):
        self.cart = {}
        self.price_list = {
            'cats': {'food': 10, 'toys': 15, 'bedding': 20},
            'dogs': {'food': 12, 'toys': 18, 'bedding': 25},
            'hamsters': {'food': 5, 'toys': 8, 'bedding': 10},
            'rabbits': {'food': 8, 'toys': 12, 'bedding': 15}
        }
        self.total_cost = 0

    def add_item(self, category, item, quantity):
        if category not in self.price_list or item not in self.price_list[category]:
            print("Invalid category or item.")
            return
        if category not in self.cart:
            self.cart[category] = {}
        if item in self.cart[category]:
            self.cart[category][item] += quantity
        else:
            self.cart[category][item] = quantity
        self.calculate_total_cost()

    def remove_item(self, category, item):
        if category in self.cart and item in self.cart[category]:
            del self.cart[category][item]
            if not self.cart[category]:
                del self.cart[category]
        self.calculate_total_cost()

    def update_item_quantity(self, category, item, quantity):
        if category in self.cart and item in self.cart[category]:
            self.cart[category][item] = quantity
        self.calculate_total_cost()

    def calculate_total_cost(self):
        self.total_cost = sum(price * quantity for category, items in self.cart.items() 
                                for item, quantity in items.items() 
                                for price in [self.price_list[category][item]])

    def display_cart(self):
        print("\nShopping Cart:")
        if not self.cart:
            print("Your cart is empty.")
            return
        for category, items in self.cart.items():
            print(category.capitalize() + ":")
            for item, quantity in items.items():
                price = self.price_list[category][item]
                print(f"{item.capitalize()}: {quantity} x £{price} = £{price * quantity}")
        print("Total Cost: £", self.total_cost)

    def save_cart(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.cart, file)

    def load_cart(self, filename):
        try:
            with open(filename, 'r') as file:
                self.cart = json.load(file)
                self.calculate_total_cost()
        except FileNotFoundError:
            print("No previous cart found.")
        except json.JSONDecodeError:
            print("Error loading cart: Invalid JSON format.")

def register():
    email = input("Enter your email address: ")
    password = input("Enter your password: ")

    with open("users.txt", "a") as file:
        file.write(f"{email}:{password}\n")
    print("Account registered successfully!")

def login():
    email = input("Enter your email address: ")
    password = input("Enter your password: ")

    try:
        with open("users.txt", "r") as file:
            users = file.readlines()
            for user in users:
                stored_email, stored_password = user.strip().split(":")
                if email == stored_email and password == stored_password:
                    print("Login successful!")
                    return True
            print("Invalid email or password.")
            return False
    except FileNotFoundError:
        print("User database not found.")
        return False

def main():
    cart = ShoppingCart()

    while True:
        print("\nWelcome to Paws for Thoughts!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()

        elif choice == "2":
            if login():
                cart.load_cart("user_cart.txt")
                while True:
                    print("\nCategories:")
                    print("1. Cats")
                    print("2. Dogs")
                    print("3. Hamsters")
                    print("4. Rabbits")
                    print("5. View Cart")
                    print("6. Save and Exit")
                    category_choice = input("Enter category choice (1-6): ")

                    if category_choice in ["1", "2", "3", "4"]:
                        category_map = {"1": "cats", "2": "dogs", "3": "hamsters", "4": "rabbits"}
                        category = category_map[category_choice]
                        print("\nItems available for", category.capitalize())
                        for item, price in cart.price_list[category].items():
                            print(f"{item.capitalize()}: £{price}")
                        item = input("Enter the item name: ").lower()
                        if item in cart.price_list[category]:
                            quantity = int(input("Enter quantity: "))
                            cart.add_item(category, item, quantity)
                        else:
                            print("Invalid item.")

                    elif category_choice == "5":
                        cart.display_cart()

                    elif category_choice == "6":
                        cart.save_cart("user_cart.txt")
                        print("Cart saved successfully. Thank you for shopping with us!")
                        break

                    else:
                        print("Invalid choice. Please try again.")

        elif choice == "3":
            print("Thank you for visiting Paws for Thoughts!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
