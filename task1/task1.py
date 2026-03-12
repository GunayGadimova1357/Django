import random

# minimum positive element
def min_positive(numbers):
    list_pos = []

    for num in numbers:
        if num > 0:
            list_pos.append(num)

    min_value = list_pos[0]

    for num in list_pos:
        if num < min_value:
            min_value = num
            
    return min_value


# maximum negative element
def max_negative(numbers):
    list_neg = []

    for num in numbers:
        if num < 0:
            list_neg.append(num)

    max_value = list_neg[0]

    for num in list_neg:
        if num > max_value:  
            max_value = num

    return max_value


# count negative numbers
def count_negative(numbers):
    count = 0

    for num in numbers:
        if num < 0:
            count += 1
    
    return count


# count positive numbers
def count_positive(numbers):
    count = 0

    for num in numbers:
        if num > 0:
            count += 1
    
    return count


# count zeros
def count_zero(numbers):
    count = 0

    for num in numbers:
        if num == 0:
            count += 1
    
    return count


numbers = []

for i in range(20):
    numbers.append(random.randint(-20, 20))


print("List:", numbers)
print("Min positive:", min_positive(numbers))
print("Max negative:", max_negative(numbers))
print("Count negative:", count_negative(numbers))
print("Count positive:", count_positive(numbers))
print("Count zero:", count_zero(numbers))