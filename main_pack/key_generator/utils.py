from flask_login import current_user
from main_pack import db, babel, gettext
from main_pack.key_generator import bp
from main_pack.models.base.models import Reg_num,Reg_num_type

from main_pack.models.hr_department.models import Employee

from main_pack.models.commerce.models import Resource
from main_pack.models.commerce.models import Res_price

from datetime import datetime
from sqlalchemy import or_, and_

prefixTypesDict = {
		'employee code':1,
		'user code':2,
		'goods code':3,
		'account code':4,
		'price code':5
	}

def generate(prefixType):
	prefixType = prefixTypesDict[prefixType]
	reg_num = Reg_num.query.filter(
		and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
	if not reg_num:
		regNumType = Reg_num_type.query.filter_by(RegNumTypeId=prefixType).first()
		RegNumPrefix = makeShortType(regNumType.RegNumTypeName_tkTM)
		newRegNum = Reg_num(UId=current_user.UId, RegNumTypeId=regNumType.RegNumTypeId,
			RegNumPrefix=RegNumPrefix,RegNumLastNum=0)
		db.session.add(newRegNum)
		db.session.commit()
	try:
		reg_num = Reg_num.query.filter(
			and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
		response = reg_num
	except:
		response = jsonify({'error':'Error generating regNo'})
	return response


def validate(fullRegNo,RegNumLastNum,prefixType):
	if(prefixType=='employee code'):
		prefixType = prefixTypesDict[prefixType]
		reg_num = Reg_num.query.filter(
			and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
		employee = Employee.query.filter_by(EmpRegNo=fullRegNo).first()

		if not employee and (RegNumLastNum>reg_num.RegNumLastNum):
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
	elif(prefixType=='goods code'):
		prefixType = prefixTypesDict[prefixType]
		reg_num = Reg_num.query.filter(
			and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
		resource = Resource.query.filter_by(ResRegNo=fullRegNo).first()

		if not resource and (RegNumLastNum>reg_num.RegNumLastNum):
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

	elif(prefixType=='price code'):
		prefixType = prefixTypesDict[prefixType]
		reg_num = Reg_num.query.filter(
			and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
		resPrice = Res_price.query.filter_by(ResPriceRegNo=fullRegNo).first()

		if not resPrice and (RegNumLastNum>reg_num.RegNumLastNum):
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
	else:
		response={
			'status':'error',
			'responseText':'Wrong prefix type or missing in database'
		}
	return response

def makeRegNum(shortName,prefix,lastNum,suffix):
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


# def validate(fullRegNo,RegNumLastNum,prefixType):
# 	prefixType = prefixTypesDict[prefixType]
# 	reg_num = Reg_num.query.filter(
# 		and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
# 	employee = Employee.query.filter_by(EmpRegNo=regNo).first()
# 	if not employee and RegNumLastNum!=reg_num.RegNumLastNum:
# 		response = {'status':True}
# 	else:
# 		response = {'status':False}
# 	return jsonify({'response':response})

###############################3
# def checkRegNo():
# 	reg_num = Reg_num.query.filter(
# 		and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
# 	req = request.get_json()
# 	regNo = req.get('regNo')
# 	employee = Employee.query.filter_by(EmpRegNo=regNo).first()
# 	if not employee:
# 		response = 'ok'
# 	else:
# 		response = 'regNo already presents'
# 	return jsonify({'response':response})