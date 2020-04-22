# from flask import render_template, url_for, json, jsonify, session, flash, redirect , request, Response, abort
# from flask_login import current_user, login_required
# from main_pack import db, babel, gettext
# from main_pack.key_generator import bp
# from main_pack.base.models import Reg_num, Reg_num_type
# from main_pack.hr_department.models import Employee,Emp_status, Profession, Nationality
# from main_pack.hr_department.models import Edu_level, Contract_type
# from datetime import datetime

# from main_pack.key_generator.utils import makeRegNum,makeShortName, makeShortType
# from sqlalchemy import or_, and_

# # @bp.route('/api/generate/')
# def generate():
# 	prefixType = 1 # 1 is for hr dep ('Ik';'Ishgar kody')
# 	# the prefixType should be changed to different thing
# 	reg_num = Reg_num.query.filter(
# 		and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
# 	if not reg_num:
# 		# the prefix creation function
# 		# finding the type of chosed prefix (hr)
# 		regNumType = Reg_num_type.query.filter_by(RegNumTypeId=prefixType).first()
# 		# parse the regNumType.RegNumTypeName_tkTM
# 		RegNumPrefix = makeShortType(regNumType.RegNumTypeName_tkTM)
# 		# !!!! add function gen function call or make this func the func
# 		# in other words it should try again
# 		# work on created modified info
# 		newRegNum = Reg_num(UId=current_user.UId, RegNumTypeId=regNumType.RegNumTypeId,
# 			RegNumPrefix=RegNumPrefix,RegNumLastNum=0)
# 		db.session.add(newRegNum)
# 		db.session.commit()
# 	try:
# 		reg_num = Reg_num.query.filter(
# 			and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
# 		regNo = makeRegNum(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum,'')
# 		# response = regNo
# 		response = reg_num
# 	except:
# 		response = jsonify({'error':'Error generating regNo'})
# 	return response

# @bp.route('/checkRegNo/',methods=['GET','POST'])
# def checkRegNo():
# 	reg_num = Reg_num.query.filter(
# 		and_(Reg_num.UId==current_user.UId,Reg_num.RegNumTypeId==prefixType)).first()
# 	# to check the method refer to
# 	# curl -i -H "Content-Type: application/json" -X POST -d '{"regNo":"1"}' http://127.0.0.1:5000/checkRegNo/
# 	req = request.get_json()
# 	# I get the json of data
# 	# like 
# 	regNo = req.get('regNo')
# 	employee = Employee.query.filter_by(EmpRegNo=regNo).first()
# 	if not employee:
# 		response = 'ok'
# 	else:
# 		response = 'regNo already presents'
# 	return jsonify({'response':response})