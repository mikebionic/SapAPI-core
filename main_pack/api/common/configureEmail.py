import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def configureEmail(input_data):
	data = None

	try:
		input_data = input_data.strip()
		if len(input_data) > 4:
			if(re.fullmatch(regex, input_data)):
				data = input_data

	except:
		pass

	return data