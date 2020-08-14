from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db_test,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce_test.admin import bp

from main_pack.models_test.base.models import Reg_num,Reg_num_type
from main_pack.key_generator.utils import makeRegNo,generate,validate

from main_pack.models_test.commerce.models import Resource
from main_pack.commerce_test.admin.utils import addResourceDict
# used foreign keys
from main_pack.models_test.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models_test.base.models import Company,Division
from main_pack.models_test.users.models import Rp_acc
####
# used relationship
from main_pack.models_test.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models_test.base.models import Image
#####

@bp.route("/ui/resource/",methods=['GET','POST','PUT'])
@login_required
def ui_resource():
	units = Unit.query.all()
	brands = Brand.query.all()
	usageStatuses = Usage_status.query.all()
	resCategories = Res_category.query.all()
	resTypes = Res_type.query.all()
	resMakers = Res_maker.query.all()
	rpAccs = Rp_acc.query.all()
	baseTemplate = {
		'units':units,
		'brands':brands,
		'usageStatuses':usageStatuses,
		'resCategories':resCategories,
		'resTypes':resTypes,
		'resMakers':resMakers,
		'rpAccs':rpAccs
		}
	reg_num = generate(UId=current_user.UId,prefixType='goods_code') # specify the generation prefix
	if request.method == "GET":
		try:
			regNo = makeRegNo(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			response = jsonify({
				'regNoForm':'resRegNo',
				'regNo':regNo
				})
		except Exception as ex:
			response = jsonify({'error':gettext('Error generating Registration number')})
		return response

	elif request.method == "POST":
		req = request.get_json()
		resource = addResourceDict(req)
		resId = req.get('resId')
		if resId == None:
			# # Method for getting the last resource if there're pre-added ones
			lastObject = Resource.query.order_by(Resource.ResId.desc()).first()
			newId = lastObject.ResId+1
			resource['ResId'] = newId

			# # validation of new resource
			fullRegNo=resource['ResRegNo']
			dbModel = Resource.query.filter_by(ResRegNo=fullRegNo).first()
			validation = validate(UId=current_user.UId,fullRegNo=fullRegNo,
				RegNumLastNum=reg_num.RegNumLastNum+1,dbModel=dbModel,prefixType='goods_code')

			if validation['status']==True:
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newResource = Resource(**resource)
				db_test.session.add(newResource)
				db_test.session.commit()
				response = jsonify({
					'resId':newResource.ResId,
					'status':'created',
					'responseText':gettext('Resource')+' '+gettext('successfully saved'),
					# 'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=newResource)
					})
			
			elif validation['status']==False:
				regNo = makeRegNo(current_user.UShortName,reg_num.RegNumPrefix,
					validation['RegNumLastNum'],'')
				resource['ResRegNo']=regNo
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newResource = Resource(**resource)
				db_test.session.add(newResource)
				db_test.session.commit()
				response = jsonify({
					'resId':newResource.ResId,
					'status':'regGenerated',
					'responseText':gettext('That registration number already presents')+'. '+gettext('It changed to ')+regNo,
					'regNoForm':'resRegNo',
					'regNo':regNo,
					})
			return response
		else:
			try:
				updateResource = Resource.query.get(int(resId))
				updateResource.update(**resource)
				updateResource.modifiedInfo(UId=current_user.UId)
				db_test.session.commit()
				response = jsonify({
					'resId':updateResource.ResId,
					'status':'updated',
					'responseText':gettext('Resource')+' '+gettext('successfully updated!'),
					})
			except Exception as ex:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
			return response


	# elif request.method == 'PUT':
	# 	req = request.get_json()
	# 	resId = req.get('resId')
	# 	currentResource = Resource.query.get(resId)
	# 	schools = School.query.filter_by(ResId=resId).order_by(School.SchoolId.desc())
	# 	workHistories = Work_history.query.filter_by(ResId=resId).order_by(Work_history.WorkHistId.desc())
	# 	awards = Award.query.filter_by(ResId=resId).order_by(Award.AwardId.desc())	
	# 	visitedCountries = Visited_countries.query.filter_by(ResId=resId).order_by(Visited_countries.VCId.desc())
	# 	relatives = Relatives.query.filter_by(ResId=resId).order_by(Relatives.RelId.desc())
	# 	thisTemplate = {
	# 		'currentResource':currentResource,
	# 		'schools':schools,
	# 		'workHistories':workHistories,
	# 		'awards':awards,
	# 		'visitedCountries':visitedCountries,
	# 		'relatives':relatives,
	# 		}
	# 	templateConfig = {
	# 		'tabTitle':(gettext("Modify employee")+' '+currentResource.EmpName),
	# 		'tabBtnClassName':'updateEmpTabBtn',
	# 		'tabBtnName':('updateEmpTabBtn'+str(currentResource.ResId)),
	# 		'tabName':('updateEmpTab'+str(currentResource.ResId)),
	# 		'tabClassName':'updateEmpTab'
	# 	}
	# 	response = {
	# 		# 'professions':professions,
	# 		'empFormNav':render_template('hr_department/empFormNav.html',**baseTemplate,**thisTemplate,**templateConfig),
	# 		'empForm':render_template('hr_department/empForm.html',**baseTemplate,**thisTemplate,**templateConfig),
	# 		'currentResource':currentResource.to_json(),
	# 		'schools':[school.to_json() for school in schools],
	# 		}
	# 	return jsonify(response)
