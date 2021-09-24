def configurePhoneNumber(number, remove_plus_sign=False):
	number = None
	try:
		number = number.strip().replace(' ','').replace('-','').replace('(','').replace(')','')

		if len(number) > 9:
			number = f"+{number}" if not remove_plus_sign and number[0] != "+" else number
			number = number[1:] if remove_plus_sign and number[0] == "+" else number

	except:
		pass

	return number