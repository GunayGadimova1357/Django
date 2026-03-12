# function to remove numbers smaller than given value
def remove_less_than(numbers, limit):
    result = []

    for num in numbers:
        if num >= limit:
            result.append(num)

    return result

numbers = []
n = int(input("How many numbers: "))

for i in range(n):
    num = int(input("Enter number: "))
    numbers.append(num)

limit = int(input("Enter the number: ")) #to remove elements less than it

new_numbers = remove_less_than(numbers, limit)

print("Result:", new_numbers)