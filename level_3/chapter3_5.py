# Handle exceptions with try-except in python / Why errors handling matters
def get_positive_integer():
    """Get a positive integer from the user."""
    while True:
        try:
            user_input=int(input("Please input a positive integer: "))
            if user_input <= 0:
                raise ValueError("The number is not positive. Please try again.")
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")
        finally:
            print("Thank you for using the calculator.")
    return user_input   


# Test the function
number = get_positive_integer()
print(f"You entered a positive integer: {number}")


