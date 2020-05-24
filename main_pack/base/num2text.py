from .en_num2text import num2text as en_num2text
from .ru_num2text import num2text as ru_num2text
from .tk_num2text import num2text as tk_num2text

def num2text(num,language='en'):
	if language=='en':
		try:
			result = en_num2text(num)
		except:
			result = "out of range"
	elif language=='ru':
		try:
			result = ru_num2text(num)
		except:
			result = "out of range"
	elif language=='tk':
		try:
			result = tk_num2text(num)
		except:
			result = "out of range"
	else:
		try:
			result = en_num2text(num)
		except:
			result = "out of range"

	return result


# print(num2text(434,'tk'))