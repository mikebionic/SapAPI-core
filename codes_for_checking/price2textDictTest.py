# -*- coding: utf-8 -*-

def price2text(language='en',currencyCode='TMT'):
	currencyCodesDict = {
		'TMT':[
						{'en':['manats','tenge']},
						{'ru':['манат','тенге']},
						{'tk':['manat','teňňe']},
					],
		'USD':[
						{'en':['dollars','cents']},
						{'ru':['долл.','центов']},
						{'tk':['dollar','sent']},
					],
		'EUR':[
						{'en':['pounds','coins']},
						{'ru':['фунтов','копеек']},
						{'tk':['funt','teňňe']},
					],
		'RUB':[
						{'en':['rub','coins']},
						{'ru':['манат','тенге']},
						{'tk':['rubl','teňňe']},
					],
	}

	try:
		for currency in currencyCodesDict:
			if currency == currencyCode:
				for languages in currencyCodesDict[currency]:
					for lang in languages:
						if lang == language:
							res = languages[lang]

	except Exception as ex:
		print(ex)
		res = ''
	return res


res = price2text('ru','TMT')

print(res[1])