############################################################################################
# Simple Calculator. Can do addition, subtraction, multiplication, division, and exponents #
############################################################################################

# Declare the first number, operator, and second number through user input


print("Can do addition (+) subtraction(-) multiplication (*) division (/) and exponents (^)")
num1 = float(input("Enter your first number: "))
op = input("Enter operator: ")
num2 = float(input("Enter your second number: "))


# Check for selected operator and if found perform operation. If not, return invalid operator


if op == "+":
    print(num1 + num2)
elif op == "-":
    print(num1 - num2)
elif op == "/":
    print(num1 / num2)
elif op == "*":
    print(num1 * num2)
elif op == "^":
    print(num1 ** num2)
else:
    print("Invalid operator")


# End of program
