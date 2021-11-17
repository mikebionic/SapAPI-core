import string
import random

def generate_random_code(use_letters = 0, length = 999999):
	data = 0
	if use_letters:
		data = ''.join(random.choices(string.ascii_letters+string.digits,k=length))
		return data

	else:
		data = random.randint(100000, length)
	
	return data