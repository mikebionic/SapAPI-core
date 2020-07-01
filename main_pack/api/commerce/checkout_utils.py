from flask import current_app

def totalQtySubstitution(totalBalance,amount):
	resultingTotal = totalBalance - amount
	print(resultingTotal)
	result = {
		'totalBalance':resultingTotal,
		'amount':amount,
		'status':1
	}
	if resultingTotal>totalBalance:
		result = {
			'totalBalance':totalBalance,
			'amount':0,
			'status':0
		}
		return result
	print(current_app.config['NEGATIVE_WH_QTY_ORDER'])
	if current_app.config['NEGATIVE_WH_QTY_ORDER']==False:
		if resultingTotal<0:
			result = {
				'totalBalance':0,
				'amount':totalBalance,
				'status':1
			}
		if totalBalance<=0:
			result = {
				'totalBalance':totalBalance,
				'amount':0,
				'status':0
			}
	return result