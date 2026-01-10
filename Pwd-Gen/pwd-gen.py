#Create a random password of a given length
'''
Needs: list of characters to choose from, 
way to randomly pick characters, a way to repeat
the picking process for the desired length
'''

#Ask user for a password length in integer only
#Define a set of characters to choose from
#Randomly pick characters from the set
#Combine picked characters into a string
#Print the genrated password

import random
import string

length = int(input("Enter password length: "))
characters = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choise(characters) for _ in range(length))
print("Generated password:", password)