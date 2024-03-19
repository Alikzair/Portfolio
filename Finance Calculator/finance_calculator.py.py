'''This Python program serves as a finance calculator, offering two main functionalities: Investment and Bond calculations. 
Users are prompted to choose between these options upon launching the program. For each option, the program collects necessary 
inputs from the user, performs the corresponding calculations, and displays the results. Error handling is implemented to 
catch any invalid inputs and provide informative error messages to the user. The program's structure is modular, 
with separate functions for each type of calculation, allowing for easy maintenance and extensibility.'''


import math

# Function to calculate investment parameters.
def calculate_investment():
    print("\nINVESTMENT CALCULATOR")
    try:
        # User input for deposit amount, interest rate, investment period, and interest type.
        deposit_amount = float(input("Enter the deposit amount: £"))
        interest_rate = float(input("Enter the interest rate (as a percentage): ")) / 100
        years = int(input("Enter the number of years you plan on investing: "))
        interest_type = input("Choose interest type ('simple' or 'compound'): ").lower()

        # Validation for valid interest type.
        if interest_type not in ['simple', 'compound']:
            raise ValueError("Invalid interest type. Please choose 'simple' or 'compound'.")

        # Calculation of total amount based on the chosen interest type.
        if interest_type == 'simple':
            total_amount = deposit_amount * (1 + interest_rate * years)
        else:
            total_amount = deposit_amount * math.pow((1 + interest_rate), years)

        # Displaying the total amount after the specified investment period.
        print(f"Total amount after {years} years: £{total_amount:.2f}")

    # Error handling for invalid inputs.
    except ValueError as e:
        print("Error:", e)
        print("Please enter valid numerical values.")

# Function to calculate bond parameters.
def calculate_bond():
    print("\nBOND CALCULATOR")
    try:
        # User input for present value of the house, interest rate, and repayment period.
        present_value = float(input("Enter the present value of the house: £"))
        interest_rate = float(input("Enter the interest rate (as a percentage): ")) / 100
        months = int(input("Enter the number of months to repay the bond: "))

        # Calculation of monthly bond repayment amount.
        monthly_payment = (interest_rate / 12 * present_value) / (1 - math.pow((1 + interest_rate / 12), -months))

        # Displaying the monthly bond repayment amount.
        print(f"Monthly bond repayment: £{monthly_payment:.2f}")

    # Error handling for invalid inputs.
    except ValueError as e:
        print("Error:", e)
        print("Please enter valid numerical values.")

# Main function to drive the program.
def main():
    print("Welcome to the Finance Calculator!\n")

    # Loop to allow multiple calculations within one session.
    while True:
        print("Choose an option:")
        print("1. Investment Calculator")
        print("2. Bond Calculator")
        print("3. Exit")

        # User choice for calculation type.
        choice = input("Enter the number of your choice: ")

        # Branching based on user choice.
        if choice == '1':
            calculate_investment()
        elif choice == '2':
            calculate_bond()
        elif choice == '3':
            print("Thank you for using the Finance Calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

# Ensuring main() is executed only if the script is run directly.
if __name__ == "__main__":
    main()
