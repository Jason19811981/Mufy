import random
adjective = ['Fearless ', 'Big ', 'Fast ']
animal = ['Cat', 'Dog', 'Horse']
number = random.randint(1,100)

name = input("What is your name?\n ")
print(name + " your code name is " + random.choice(adjective) + random.choice(animal))
print(f"Your lucky number is: {number}")