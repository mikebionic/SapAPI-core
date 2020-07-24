from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.models.base.models import Reg_num,Reg_num_type
from main_pack.key_generator.utils import makeRegNo,generate,validate

from main_pack.models.commerce.models import Res_price
from main_pack.commerce.admin.utils import addResPriceDict

# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models.base.models import Company,Division
from main_pack.models.users.models import Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Unit,Res_unit,Inv_line,Inv_line_det,Order_inv_line,
	Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,Sale_agr_res_price,Res_discount)
#####

@bp.route("/ui/price/",methods=['GET','POST','PUT'])
@login_required
def ui_price():
	reg_num = generate(UId=current_user.UId,prefixType='price_code') # specify the generation prefix
	if request.method == "GET":
		try:
			regNo = makeRegNo(current_user.UShortName,reg_num.RegNumPrefix,reg_num.RegNumLastNum+1,'')
			response = jsonify({
				'regNoForm':'resPriceRegNo',
				'regNo':regNo
				})
		except:
			response = jsonify({'error':gettext('Error generating Registration number')})
		return response

	elif request.method == "POST":
		req = request.get_json()
		resPrice = addResPriceDict(req)
		resPriceId = req.get('resPriceId')
		if resPriceId == None:

			lastObject = Res_price.query.order_by(Res_price.ResPriceId.desc()).first()
			newId = lastObject.ResPriceId+1
			resPrice['ResPirceId'] = newId

			fullRegNo=resPrice['ResPriceRegNo']
			dbModel = Res_price.query.filter_by(ResRegNo=fullRegNo).first()

			validation = validate(UId=current_user.UId,fullRegNo=fullRegNo,
				RegNumLastNum=reg_num.RegNumLastNum+1,dbModel=dbModel,prefixType='price_code')
			if validation['status']==True:
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newResPrice = Res_price(**resPrice)
				db.session.add(newResPrice)
				db.session.commit()
				response = jsonify({
					'resPriceId':newResPrice.ResPriceId,
					'status':'created',
					'responseText':gettext('Price')+' '+gettext('successfully saved!')
					})
			
			elif validation['status']==False:
				regNo = makeRegNo(current_user.UShortName,reg_num.RegNumPrefix,
					validation['RegNumLastNum'],'')
				resPrice['ResPriceRegNo']=regNo
				reg_num.RegNumLastNum=validation['RegNumLastNum']
				newResPrice = Res_price(**resPrice)
				db.session.add(newResPrice)
				db.session.commit()
				response = jsonify({
					'resPriceId':newResPrice.ResPriceId,
					'status':'regGenerated',
					'responseText':gettext('That registration number already presents')+'. '+gettext('It changed to ')+regNo,
					'regNoForm':'resPriceRegNo',
					'regNo':regNo
					})
			return response
		else:
			try:
				updateResPrice = Res_price.query.get(int(resPriceId))
				updateResPrice.update(**resPrice)
				updateResPrice.modifiedInfo(UId=current_user.UId)
				db.session.commit()
				response = jsonify({
					'resPriceId':updateResPrice.ResPriceId,
					'status':'updated',
					'responseText':gettext('Price')+' '+gettext('successfully updated!'),
					# 'data': render_template('/hr_department/tableEmpAppend.html',**baseTemplate,employee=updateResPrice),
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
			return response
