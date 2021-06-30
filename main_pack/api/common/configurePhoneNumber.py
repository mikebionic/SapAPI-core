def configurePhoneNumber(number, with_plus_sign=False):
	number = number.strip().replace(' ','').replace('-','').replace('(','').replace(')','')

	if len(number) > 9:
		number = f"+{number}" if with_plus_sign and number[0] != "+" else number
		number = number[1:] if not with_plus_sign and number[0] == "+" else number

	else:
		number = None

	return number