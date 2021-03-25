State = False
def totalQtySubstitution(totalBalance,amount):
	resultingTotal = totalBalance - amount
	print(resultingTotal)
	result = {
		'totalBalance':resultingTotal,
		'amount':amount
	}
	if resultingTotal>totalBalance:
		print('error resulting greater')
		result = {
			'totalBalance':totalBalance,
			'amount':0
		}
		return result

	if State==False:
		if resultingTotal<0:
			print('total is less than 0')
			result = {
				'totalBalance':0,
				'amount':totalBalance
			}
		if totalBalance<=0:
			print('condition')
			result = {
				'totalBalance':totalBalance,
				'amount':0
			}
	return result


res = totalQtySubstitution(8,1)

print(res)