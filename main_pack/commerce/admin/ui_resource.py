from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime

from main_pack.models.base.models import Reg_num,Reg_num_type
from main_pack.key_generator.utils import makeRegNum,generate,validate

from main_pack.models.base.models import Resource
# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status
from main_pack.models.base.models import Company,Division,Res_category,Resource_type,Resource_maker,Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image
#####

@bp.route("/ui/resource/",methods=['GET','POST','PUT'])
@login_required
def ui_resource():
	units = Unit.query.all()
	brands = Brand.query.all()
	usageStatuses = Usage_status.query.all()
	resCategories = Res_category.query.all()
	resourceTypes = Resource_type.query.all()
	resourceMakers = Resource_maker.query.all()
	rpAccs = Rp_acc.query.all()
	baseTemplate = {
		'units':units,
		'brands':brands,
		'usageStatuses':usageStatuses,
		'resCategories':resCategories,
		'resourceTypes':resourceTypes,
		'resourceMakers':resourceMakers,
		'rpAccs':rpAccs
		}
	reg_num = generate('goods code') # specify the generation prefix
	if request.method == "GET":
		try:
			regNo = makeRegNum(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			response = regNo
		except:
			response = jsonify({'error':gettext('Error generating Registration number')})
		return response

	elif request.method == "POST":
		req = request.get_json()
		employee = addEmpDict(req)
		empId = req.get('empId')
		if empId == None:
			validation = validate(employee['EmpRegNo'],reg_num.RegNumLastNum+1,prefixType='employee code')

			if validation['status']==True:
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newEmployee = Employee(**employee)
				db.session.add(newEmployee)
				db.session.commit()
				response = jsonify({
					'empId':newEmployee.EmpId,
					'status':'created',
					'responseText':gettext('Employee')+' '+gettext('successfully saved!'),
					'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=newEmployee)
					})
			
			elif validation['status']==False:
				regNo = makeRegNum(current_user.UShortName,reg_num.RegNumPrefix,
					validation['RegNumLastNum'],'')
				employee['EmpRegNo']=regNo
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newEmployee = Employee(**employee)
				db.session.add(newEmployee)
				db.session.commit()
				response = jsonify({
					'empId':newEmployee.EmpId,
					'status':'regGenerated',
					'responseText':'That registration number already presents. It changed to '+regNo,
					'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=newEmployee)
					})
			return response
		else:
			try:
				updateEmployee = Employee.query.get(int(empId))
				updateEmployee.update(**employee)
				updateEmployee.modifiedInfo(UId=current_user.UId)
				db.session.commit()
				response = jsonify({
					'empId':updateEmployee.EmpId,
					'status':'updated',
					'responseText':gettext('Employee')+' '+gettext('successfully updated!'),
					'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=updateEmployee),
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
			return response
	elif request.method == 'PUT':
		req = request.get_json()
		empId = req.get('empId')
		currentEmployee = Employee.query.get(empId)
		schools = School.query.filter_by(EmpId=empId).order_by(School.SchoolId.desc())
		workHistories = Work_history.query.filter_by(EmpId=empId).order_by(Work_history.WorkHistId.desc())
		awards = Award.query.filter_by(EmpId=empId).order_by(Award.AwardId.desc())	
		visitedCountries = Visited_countries.query.filter_by(EmpId=empId).order_by(Visited_countries.VCId.desc())
		relatives = Relatives.query.filter_by(EmpId=empId).order_by(Relatives.RelId.desc())
		thisTemplate = {
			'currentEmployee':currentEmployee,
			'schools':schools,
			'workHistories':workHistories,
			'awards':awards,
			'visitedCountries':visitedCountries,
			'relatives':relatives,
			}
		templateConfig = {
			'tabTitle':(gettext("Modify employee")+' '+currentEmployee.EmpName),
			'tabBtnClassName':'updateEmpTabBtn',
			'tabBtnName':('updateEmpTabBtn'+str(currentEmployee.EmpId)),
			'tabName':('updateEmpTab'+str(currentEmployee.EmpId)),
			'tabClassName':'updateEmpTab'
		}
		response = {
			# 'professions':professions,
			'empFormNav':render_template('hr_department/empFormNav.html',**baseTemplate,**thisTemplate,**templateConfig),
			'empForm':render_template('hr_department/empForm.html',**baseTemplate,**thisTemplate,**templateConfig),
			'currentEmployee':currentEmployee.to_json(),
			'schools':[school.to_json() for school in schools],
			}
		return jsonify(response)



# @bp.route("/ui/employee/", methods=['GET','POST','PUT'])
# @login_required
# def uiEmployee():
# 	professions = Profession.query.all()
# 	departments = Department.query.all()
# 	nationalities = Nationality.query.all()
# 	genders = Gender.query.all()
# 	contractTypes = Contract_type.query.all()
# 	eduLevels = Edu_level.query.all()
# 	empStatuses = Emp_status.query.all()
# 	schoolTypes = School_type.query.all()
# 	relStatuses = Rel_status.query.all()
# 	baseTemplate = {
# 		'professions':professions,
# 		'departments':departments,
# 		'nationalities':nationalities,
# 		'genders':genders,
# 		'contractTypes':contractTypes,
# 		'eduLevels':eduLevels,
# 		'empStatuses':empStatuses,
# 		'schoolTypes':schoolTypes,
# 		'relStatuses':relStatuses
# 		}
# 	reg_num = generate('employee code') # specify the generation prefix
# 	if request.method == "GET":
# 		try:
# 			regNo = makeRegNum(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
# 			response = regNo
# 		except:
# 			response = jsonify({'error':gettext('Error generating Registration number')})
# 		return response

# 	elif request.method == "POST":
# 		req = request.get_json()
# 		employee = addEmpDict(req)
# 		empId = req.get('empId')
# 		if empId == None:
# 			validation = validate(employee['EmpRegNo'],reg_num.RegNumLastNum+1,prefixType='employee code')

# 			if validation['status']==True:
# 				reg_num.RegNumLastNum=validation['RegNumLastNum']
# 				newEmployee = Employee(**employee)
# 				db.session.add(newEmployee)
# 				db.session.commit()
# 				response = jsonify({
# 					'empId':newEmployee.EmpId,
# 					'status':'created',
# 					'responseText':gettext('Employee')+' '+gettext('successfully saved!'),
# 					'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=newEmployee)
# 					})
			
# 			elif validation['status']==False:
# 				regNo = makeRegNum(current_user.UShortName,reg_num.RegNumPrefix,
# 					validation['RegNumLastNum'],'')
# 				employee['EmpRegNo']=regNo
# 				reg_num.RegNumLastNum=validation['RegNumLastNum']
# 				newEmployee = Employee(**employee)
# 				db.session.add(newEmployee)
# 				db.session.commit()
# 				response = jsonify({
# 					'empId':newEmployee.EmpId,
# 					'status':'regGenerated',
# 					'responseText':'That registration number already presents. It changed to '+regNo,
# 					'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=newEmployee)
# 					})
# 			return response
# 		else:
# 			try:
# 				updateEmployee = Employee.query.get(int(empId))
# 				updateEmployee.update(**employee)
# 				updateEmployee.modifiedInfo(UId=current_user.UId)
# 				db.session.commit()
# 				response = jsonify({
# 					'empId':updateEmployee.EmpId,
# 					'status':'updated',
# 					'responseText':gettext('Employee')+' '+gettext('successfully updated!'),
# 					'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=updateEmployee),
# 					})
# 			except:
# 				response = jsonify({
# 					'status':'error',
# 					'responseText':gettext('Unknown error!'),
# 					})
# 			return response
# 	elif request.method == 'PUT':
# 		req = request.get_json()
# 		empId = req.get('empId')
# 		currentEmployee = Employee.query.get(empId)
# 		schools = School.query.filter_by(EmpId=empId).order_by(School.SchoolId.desc())
# 		workHistories = Work_history.query.filter_by(EmpId=empId).order_by(Work_history.WorkHistId.desc())
# 		awards = Award.query.filter_by(EmpId=empId).order_by(Award.AwardId.desc())	
# 		visitedCountries = Visited_countries.query.filter_by(EmpId=empId).order_by(Visited_countries.VCId.desc())
# 		relatives = Relatives.query.filter_by(EmpId=empId).order_by(Relatives.RelId.desc())
# 		thisTemplate = {
# 			'currentEmployee':currentEmployee,
# 			'schools':schools,
# 			'workHistories':workHistories,
# 			'awards':awards,
# 			'visitedCountries':visitedCountries,
# 			'relatives':relatives,
# 			}
# 		templateConfig = {
# 			'tabTitle':(gettext("Modify employee")+' '+currentEmployee.EmpName),
# 			'tabBtnClassName':'updateEmpTabBtn',
# 			'tabBtnName':('updateEmpTabBtn'+str(currentEmployee.EmpId)),
# 			'tabName':('updateEmpTab'+str(currentEmployee.EmpId)),
# 			'tabClassName':'updateEmpTab'
# 		}
# 		response = {
# 			# 'professions':professions,
# 			'empFormNav':render_template('hr_department/empFormNav.html',**baseTemplate,**thisTemplate,**templateConfig),
# 			'empForm':render_template('hr_department/empForm.html',**baseTemplate,**thisTemplate,**templateConfig),
# 			'currentEmployee':currentEmployee.to_json(),
# 			'schools':[school.to_json() for school in schools],
# 			}
# 		return jsonify(response)



@bp.route('/ui/award/', methods=['GET','POST','PUT'])
def addAward():
	if request.method == 'POST':
		req = request.get_json()
		award = addAwardDict(req)
		awardId = req.get('awardId')
		if (awardId == '' or awardId == None):
			newAward = Award(**award)
			db.session.add(newAward)
			db.session.commit()
			response = jsonify({
				'awardId':newAward.AwardId,
				'status':'created',
				'responseText':gettext('Award')+' '+gettext('successfully saved'),
				'data': render_template('/hr_department/tableAwardAppend.html',award=newAward)
				})
		else:
			try:
				updateAward = Award.query.get(int(awardId))
				updateAward.update(**award)
				updateAward.modifiedInfo(UId=current_user.UId)
				db.session.commit()
				response = jsonify({
						'awardId':updateAward.AwardId,
						'status':'updated',
						'responseText':gettext('Award')+' '+gettext('successfully updated'),
						'data': render_template('/hr_department/tableAwardAppend.html',award=updateAward)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	if request.method == 'PUT':
		req = request.get_json()
		awardId = req.get('awardId')
		thisAward = Award.query.get(awardId)
		response = {
			'awardId':awardId,
			'thisAward':thisAward.to_json()
		}


### restapi get requestsssss json
# generalData = {"employee":{
#     "username":"planP",
#     "password":"12345"
# },
# "schools" : [
#     {    
#         "empId":"123",
#         "name":"martin"
#     },
#     {
#         "empId":"123",
#         "name":"martin"
#     }
# ]
# }
# for (data in generalData.schools){
#     console.log(generalData.schools[data])
# }
#################



# @bp.route("/employee/empForm/", methods=['GET'])
# # @login_required
# def empForm():
# 	professions = Profession.query.all()
# 	departments = Department.query.all()
# 	nationalities = Nationality.query.all()
# 	genders = Gender.query.all()
# 	contractTypes = Contract_type.query.all()
# 	eduLevels = Edu_level.query.all()
# 	empStatuses = Emp_status.query.all()
# 	schoolTypes = School_type.query.all()
# 	relStatuses = Rel_status.query.all()
# 	schools = []
# 	workHistories = []
# 	awards = []
# 	visitedCountries = []
# 	relatives = []
# 	baseTemplate = {
# 		'professions':professions,
# 		'departments':departments,
# 		'nationalities':nationalities,
# 		'genders':genders,
# 		'contractTypes':contractTypes,
# 		'eduLevels':eduLevels,
# 		'empStatuses':empStatuses,
# 		'schoolTypes':schoolTypes,
# 		'relStatuses':relStatuses,
# 		'schools':schools,
# 		'workHistories':workHistories,
# 		'awards':awards,
# 		'visitedCountries':visitedCountries,
# 		'relatives':relatives,
# 		}
# 	templateConfig = {
# 		'tabTitle':gettext("New employee"),
# 		'tabBtnClassName':'addEmpTabBtn',
# 		'tabBtnName':'addEmpTabBtn',
# 		'tabName':'addEmpTab',
# 		'tabClassName':'addEmpTab'
# 	}
# 	return jsonify({
# 		'empForm':render_template("hr_department/empForm.html",**baseTemplate,**templateConfig),
# 		'empFormNav':render_template("hr_department/empFormNav.html",**baseTemplate,**templateConfig)
# 		})
