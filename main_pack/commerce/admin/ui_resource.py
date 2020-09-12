from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.models.base.models import Reg_num,Reg_num_type
from main_pack.key_generator.utils import makeRegNo,generate,validate

from main_pack.models.commerce.models import Resource
from main_pack.commerce.admin.utils import addResourceDict
# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models.base.models import Company,Division
from main_pack.models.users.models import Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image
#####

@bp.route("/ui/resource/",methods=['GET','POST','PUT'])
@login_required
@ui_admin_required()
def ui_resource():
	units = Unit.query.all()
	brands = Brand.query.all()
	usageStatuses = Usage_status.query.all()
	resCategories = Res_category.query.all()
	resTypes = Res_type.query.all()
	resMakers = Res_maker.query.all()
	rpAccs = Rp_acc.query.all()
	baseTemplate = {
		"units": units,
		"brands": brands,
		"usageStatuses": usageStatuses,
		"resCategories": resCategories,
		"resTypes": resTypes,
		"resMakers": resMakers,
		"rpAccs": rpAccs
		}
	reg_num = generate(UId=current_user.UId,RegNumTypeName='goods_code') # specify the generation prefix
	if request.method == 'GET':
		try:
			regNo = makeRegNo(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			response = jsonify({
				"regNoForm": 'resRegNo',
				"regNo": regNo
				})
		except Exception as ex:
			print(ex)
			response = jsonify({"error": gettext('Error generating Registration number')})
		return response

	elif request.method == 'POST':
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
				RegNumLastNum=reg_num.RegNumLastNum+1,dbModel=dbModel,RegNumTypeName='goods_code')

			if validation['status']==True:
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newResource = Resource(**resource)
				db.session.add(newResource)
				db.session.commit()
				response = jsonify({
					"resId": newResource.ResId,
					"status": "created",
					"responseText": gettext('Resource')+' '+gettext('successfully saved'),
					# "data":  render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=newResource)
					})
			
			elif validation['status']==False:
				regNo = makeRegNo(current_user.UShortName,
													reg_num.RegNumPrefix,
													validation['RegNumLastNum'],'')
				resource['ResRegNo']=regNo
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newResource = Resource(**resource)
				db.session.add(newResource)
				db.session.commit()
				response = jsonify({
					"resId": newResource.ResId,
					"status": "regGenerated",
					"responseText": gettext('That registration number already presents')+'. '+gettext('It changed to ')+regNo,
					"regNoForm": "resRegNo",
					"regNo": regNo,
					})
			return response
		else:
			try:
				updateResource = Resource.query.get(int(resId))
				updateResource.update(**resource)
				updateResource.modifiedInfo(UId=current_user.UId)
				db.session.commit()
				response = jsonify({
					"resId": updateResource.ResId,
					"status": "updated",
					"responseText": gettext('Resource')+' '+gettext('successfully updated!'),
					})
			except Exception as ex:
				print(ex)
				response = jsonify({
					"status": "error",
					"responseText": gettext('Unknown error!'),
					})
			return response