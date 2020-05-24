# -*- coding: utf-8 -*-

import decimal

languages = {
	'tk':{
		'units':(
			u'nol',

			(u'bir', u'bir'),
			(u'iki', u'iki'),

			u'üç', u'dört', u'bäş',
			u'alty', u'ýedi', u'sekiz', u'dokuz'
		),
		'teens':(
			u'on', u'on bir',
			u'on iki', u'on üç',
			u'on dört', u'on bäş',
			u'on alty', u'on ýedi',
			u'on sekiz', u'on dokuz'
		),
		'tens':(
			u'ýigrimi', u'otuz',
			u'kyrk', u'elli',
			u'altmyş', u'ýetmiş',
			u'segsen', u'togsan'
		),
		'hundreds':(
			u'ýüz', u'iki ýüz',
			u'üç ýüz', u'dört ýüz',
			u'bäş ýüz', u'alty ýüz',
			u'ýedi ýüz', u'sekiz ýüz',
			u'dokuz ýüz'
		),
		'orders':[
			((u'müň', u'müň', u'müň'), 'f'),
			((u'million', u'million', u'million'), 'm'),
			((u'milliard', u'milliard', u'milliard'), 'm'),
			((u'quintillion', u'quintillion', u'quintillion'), 'm'),
			((u'septillion', u'septillion', u'septillion'), 'm'),
			((u'nonillion', u'nonillion', u'nonillion'), 'm'),
			((u'undecillion', u'undecillion', u'undecillion'), 'm'),
		],
		'minus':u'minus'
	}
}

def thousand(rest,sex,language):
	units = languages[language]['units']
	teens = languages[language]['teens']
	tens = languages[language]['tens']
	hundreds = languages[language]['hundreds']
	orders = languages[language]['orders']

		
	prev = 0
	plural = 2
	name = []
	use_teens = rest % 100 >= 10 and rest % 100 <= 19
	if not use_teens:
		data = ((units, 10), (tens, 100), (hundreds, 1000))
	else:
		data = ((teens, 10), (hundreds, 1000))
	for names, x in data:
		cur = int(((rest - prev) % x) * 10 / x)
		prev = rest % x
		if x == 10 and use_teens:
			plural = 2
			name.append(teens[cur])
		elif cur == 0:
			continue
		elif x == 10:
			name_ = names[cur]
			if isinstance(name_, tuple):
				name_ = name_[0 if sex == 'm' else 1]
			name.append(name_)
			if cur >= 2 and cur <= 4:
				plural = 1
			elif cur == 1:
				plural = 0
			else:
				plural = 2
		else:
			name.append(names[cur-1])
	return plural, name


def num2text(num,language, main_units=((u'', u'', u''), 'm')):
	orders = languages[language]['orders']
	global ordersGlobal
	ordersGlobal = languages[language]['orders']
	ordersGlobal = (main_units,) + orders
	if num == 0:
		return ' '.join((units[0], ordersGlobal[0][0][2])).strip() # ноль
	rest = abs(num)
	ord = 0
	name = []
	while rest > 0:
		plural, nme = thousand(rest % 1000, ordersGlobal[ord][1],language)
		if nme or ord == 0:
			name.append(ordersGlobal[ord][0][plural])
		name += nme
		rest = int(rest / 1000)
		ord += 1
	if num < 0:
		name.append(minus)
	name.reverse()
	return ' '.join(name).strip()


def decimal2text(value, places=2,
				 int_units=(('', '', ''), 'm'),
				 exp_units=(('', '', ''), 'm')):
	value = decimal.Decimal(value)
	q = decimal.Decimal(10) ** -places

	integral, exp = str(value.quantize(q)).split('.')
	return u'{} {}'.format(
		num2text(int(integral), int_units),
		num2text(int(exp), exp_units))

if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		try:
			num = sys.argv[1]
			if '.' in num:
				print(decimal2text(
					decimal.Decimal(num),
					int_units=((u'штука', u'штуки', u'штук'), 'f'),
					exp_units=((u'кусок', u'куска', u'кусков'), 'm')))
			else:
				print(num2text(
					int(num),
					main_units=((u'штука', u'штуки', u'штук'), 'f')))
		except ValueError:
			print (sys.stderr, "Invalid argument {}".format(sys.argv[1]))
		sys.exit()



print(num2text(45342,'tk'))
print(num2text(15112,'tk'))
print(num2text(798357344,'tk'))
print(num2text(33776666288390,'tk'))
print(num2text(498509298616416395985363,'tk'))