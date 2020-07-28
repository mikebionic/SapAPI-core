from flask import current_app
from flask_login import current_user
from main_pack import db, babel, gettext
from main_pack.key_generator import bp
from main_pack.models.base.models import Reg_num,Reg_num_type

from main_pack.models.hr_department.models import Employee
from main_pack.models.users.models import Users

from datetime import datetime
from sqlalchemy import or_, and_
from random import randint

prefixTypesDict = {
		'employee_code':1,
		'user_code':2,
		'goods_code':3,
		'account_code':4,
		'price_code':5,
		'rp_code':6,
		'sale_invoice_code':7,
		'purchase_invoice_code':8,
		'sale_order_invoice_code':9,
		'purchase_order_invoice_code':10,
		'sale_return_invoice_code':11,
		'purchase_return_invoice_code':12,
		'order_invoice_line_code':13,
		'invoice_line_code':14
	}

def generate(UId,prefixType):
	# user = Users.query.get(UId)
	prefixType = prefixTypesDict[prefixType]
	reg_num = Reg_num.query.filter(
		and_(Reg_num.UId==UId,Reg_num.RegNumTypeId==prefixType)).first()
	if not reg_num:
		regNumType = Reg_num_type.query.filter_by(RegNumTypeId=prefixType).first()
		RegNumPrefix = makeShortType(regNumType.RegNumTypeName_tkTM)
		newRegNum = Reg_num(UId=UId, RegNumTypeId=regNumType.RegNumTypeId,
			RegNumPrefix=RegNumPrefix,RegNumLastNum=0)
		db.session.add(newRegNum)
		db.session.commit()
	# try:
	reg_num = Reg_num.query.filter(
		and_(Reg_num.UId==UId,Reg_num.RegNumTypeId==prefixType)).first()
	response = reg_num
	# except Exception as ex:
	# 	response = jsonify({'error':'Error generating regNo'})
	return response

def validate(UId,fullRegNo,RegNumLastNum,dbModel,prefixType):
	# user = Users.query.get(UId)
	try:
		prefixType = prefixTypesDict[prefixType]
		reg_num = Reg_num.query.filter(
			and_(Reg_num.UId==UId,Reg_num.RegNumTypeId==prefixType)).first()
		if not dbModel and (RegNumLastNum>reg_num.RegNumLastNum):
			response = {
				'status':True,
				'RegNumLastNum':RegNumLastNum
			}
		else:
			while RegNumLastNum<=reg_num.RegNumLastNum:
				RegNumLastNum+=1
			response = {
				'status':False,
				'RegNumLastNum':RegNumLastNum
			}
	except Exception as ex:
		response={
			'status':'error',
			'responseText':'Wrong prefix type or missing in database'
		}
	return response

def makeRegNo(shortName,prefix,lastNum,suffix,random_mode=None):
	if random_mode:
		lastNum = randint(1,current_app.config['REG_NUM_RANDOM_RANGE'])
	regNo = shortName+prefix+str(lastNum)+suffix
	return regNo
	
# returnes first leters of typeName
def makeShortType(text):
	words = text.split()
	short = [word[0] for word in words]
	short = (''.join(short)).upper()
	return short

# returnes first and last letter of UName
def makeShortName(name):
	short = (name[0]+name[-1]).upper()
	return short