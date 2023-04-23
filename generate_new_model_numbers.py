import random
import string

# Define the length of the random string
string_length = 16

# Define the character set for the random string
character_set = string.ascii_letters + string.digits

# Generate a list of 10 random strings
random_strings = []
for i in range(10):
    random_string = ''.join(random.choices(character_set, k=string_length))
    random_strings.append(random_string)

print(random_strings)

