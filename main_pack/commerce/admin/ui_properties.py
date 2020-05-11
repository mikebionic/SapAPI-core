from flask import render_template,url_for,jsonify,json,session,flash,redirect,request,abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import addColorDict,addSizeDict,addBrandDict,addResColorDict,addResSizeDict
from main_pack.models.commerce.models import Color,Size,Size_type,Unit,Brand,Barcode

from main_pack.models.commerce.models import Size_type,Res_color,Res_size,Res_unit,Usage_status


@bp.route('/ui/color/', methods=['GET','POST','PUT'])
def ui_color():
	if request.method == 'POST':
		# respon 
		req = request.get_json()
		color = addColorDict(req)
		print(color)

		colorId = req.get('colorId')
		print(colorId)
		if (colorId == '' or colorId == None):
			try:
				print('committing')
				newColor = Color(**color)
				db.session.add(newColor)
				db.session.commit()
				response = jsonify({
					'colorId':newColor.ColorId,
					'status':'created',
					'responseText':gettext('Color')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/colorAppend.html',color=newColor)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	return response

@bp.route('/ui/size/', methods=['POST','PUT'])
def ui_size():
	if request.method == 'POST':
		req = request.get_json()
		size = addSizeDict(req)
		sizeId = req.get('sizeId')
		if (sizeId == '' or sizeId == None):
			try:
				newSize = Size(**size)
				db.session.add(newSize)
				db.session.commit()
				response = jsonify({
					'sizeId':newSize.SizeId,
					'status':'created',
					'responseText':gettext('Size')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/sizeAppend.html',size=newSize)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	return response

@bp.route('/ui/brand/', methods=['POST','PUT'])
def ui_brand():
	if request.method == 'POST':
		req = request.get_json()
		brand = addBrandDict(req)
		brandId = req.get('brandId')
		if (brandId == '' or brandId == None):
			try:
				newBrand = Brand(**brand)
				db.session.add(newBrand)
				db.session.commit()
				response = jsonify({
					'brandId':newBrand.BrandId,
					'status':'created',
					'responseText':gettext('Brand')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/brandAppend.html',brand=newBrand)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	return response

@bp.route('/ui/res_color/', methods=['GET','POST','PUT'])
def ui_res_color():
	if request.method == 'POST':
		req = request.get_json()
		try:
			for resColorReq in req:
				resColor = addResColorDict(resColorReq)
				print(resColor)
				rcId = resColor.get('rcId')
				if (rcId == '' or rcId == None):
					newResColor = Res_color(**resColor)
					db.session.add(newResColor)
					db.session.commit()
			response=jsonify({
				'status':'created',
				'responseText':gettext('Product colors')+' '+gettext('successfully saved'),
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	if request.method == 'DELETE':
		req = request.get_json()
		rcId = req.get('rcId')
		thisResColor = Res_color.query.get(rcId)
		thisResColor.GCRecord == 1
		response = jsonify({
			'rcId':thisResColor.RcId,
			'status':'deleted',
			'responseText':gettext('Product colors')+' '+gettext('successfully deleted')
		})
	return response


@bp.route('/ui/res_size/', methods=['GET','POST','PUT'])
def ui_res_size():
	if request.method == 'POST':
		req = request.get_json()
		responses=[]
		try:
			for resColorReq in req:
				resColor = addResColorDict(resColorReq)
				print(resColor)
				rcId = resColor.get('rcId')
				if (rcId == '' or rcId == None):
					newResColor = Res_color(**resColor)
					db.session.add(newResColor)
					db.session.commit()
					response = {
						'rcId':newResColor.RcId,
						'fileName':newResColor.FileName,
						}
					responses.append(response)
			
			fullResponse={
				'status':'created',
				'responseText':gettext('Product colors')+' '+gettext('successfully saved'),
				}
			fullResponse['responses']=responses
			response = fullResponse
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})
		print('end response is ')
		print(response)

	if request.method == 'DELETE':
		req = request.get_json()
		rcId = req.get('rcId')
		thisResColor = Res_color.query.get(rcId)
		thisResColor.GCRecord == 1
		response = jsonify({
			'rcId':thisResColor.RcId,
			'status':'deleted',
			'responseText':gettext('Product colors')+' '+gettext('successfully deleted')
		})
	return response


	# <script> 
 #        $('#GFG_UP') 
 #        .text('First check few elements then click on the button.'); 
 #        $('button').on('click', function() { 
 #            var array = []; 
 #            $("input:checkbox[name=type]:checked").each(function() { 
 #                array.push($(this).val()); 
 #            }); 
 #            $('#GFG_DOWN').text(array); 
 #        }); 
 #    </script> 