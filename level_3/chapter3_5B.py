def get_number_between_zero_and_one():

    while True:
        try:
            user_input = float(input("Please input a number between 0 and 1: "))
            if user_input < 0 or user_input > 1:
                raise ValueError("The number is not between 0 and 1. Please try again.")
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")
        finally:
            print("Thank you for using the calculator.")


number = get_number_between_zero_and_one()
print(f"You entered a valid number between 0 and 1: {number}")
