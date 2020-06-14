from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp
from main_pack.models.commerce.models import Resource,Res_category


from main_pack.models.base.models import Company

# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models.base.models import Company,Division,Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image
#####
from main_pack.models.base.models import Language
from main_pack.models.commerce.models import Color,Size,Brand

from main_pack.models.commerce.models import Resource 


def commonUsedData():
	commonData = {}
	subcategories = []
	subcategory_children = []
	company = Company.query.get(1)
	categories = Res_category.query.filter_by(ResOwnerCatId=0)
	subcategory = Res_category.query.filter(Res_category.ResOwnerCatId!=0)
	for category in subcategory:
		parents = Res_category.query.filter(Res_category.ResCatId==category.ResOwnerCatId)
		for parent in parents:
			if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
				subcategories.append(category)
			else:
				subcategory_children.append(category)

	commonData.update({
		"categories":categories,
		"subcategories":subcategories,
		"subcategory_children":subcategory_children,
		"company":company
		})
	return commonData


from main_pack.base.apiMethods import fileToURL

@bp.route("/v-list")
def v_list():
	resources = Resource.query\
		.filter(Resource.GCRecord=='' or Resource.GCRecord==None).all()
	barcodes = Barcode.query\
		.filter(Barcode.GCRecord=='' or Barcode.GCRecord==None).all()
	categories = Res_category.query\
		.filter(Res_category.GCRecord=='' or Res_category.GCRecord==None).all()
	res_prices = Res_price.query\
		.filter(Res_price.GCRecord=='' or Res_price.GCRecord==None).all()
	res_totals = Res_total.query\
		.filter(Res_total.GCRecord=='' or Res_total.GCRecord==None).all()
	images = Image.query\
		.filter(Image.GCRecord=='' or Image.GCRecord==None).all()

	colors = Color.query\
		.filter(Color.GCRecord=='' or Color.GCRecord==None).all()
	sizes = Size.query\
		.filter(Size.GCRecord=='' or Size.GCRecord==None).all()
	brands = Brand.query\
		.filter(Brand.GCRecord=='' or Brand.GCRecord==None).all()

	res_colors = Res_color.query\
		.filter(Res_color.GCRecord=='' or Res_color.GCRecord==None).all()
	res_sizes = Res_size.query\
		.filter(Res_size.GCRecord=='' or Res_size.GCRecord==None).all()

	data = []
	for resource in resources:
		resourceList = resource.to_json_api()

		List_Barcode = [barcode.BarcodeVal for barcode in barcodes if barcode.ResId==resource.ResId]
		List_Res_category = [category.ResCatName for category in categories if category.ResCatId==resource.ResCatId]
		List_Res_price = [res_price.ResPriceValue for res_price in res_prices if res_price.ResId==resource.ResId and res_price.ResPriceTypeId==2]
		List_Res_total = [res_total.ResTotBalance for res_total in res_totals if res_total.ResId==resource.ResId]
		List_FileName = [image.FileName for image in images if image.ResId==resource.ResId]

		List_Colors = [color for res_color in res_colors if res_color.ResId==resource.ResId for color in colors if color.ColorId==res_color.ColorId]
		List_Sizes = [size for res_size in res_sizes if res_size.ResId==resource.ResId for size in sizes if size.SizeId==res_size.SizeId]
		List_Brands = [brand for brand in brands if brand.BrandId==resource.BrandId]

		resourceList["BarcodeVal"] = List_Barcode[0] if len(List_Barcode)>0 else ''
		resourceList["ResCatName"] = List_Res_category[0] if len(List_Res_category)>0 else ''
		resourceList["ResPriceValue"] = List_Res_price[0] if len(List_Res_price)>0 else ''
		resourceList["ResTotBalance"] = List_Res_total[0] if len(List_Res_total)>0 else ''
		resourceList["FilePathS"] = fileToURL('S',List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathM"] = fileToURL('M',List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathR"] = fileToURL('R',List_FileName[0]) if len(List_FileName)>0 else ''

		resourceList["Colors"] = List_Colors if len(List_Colors)>0 else ''
		resourceList["Sizes"] = List_Sizes if len(List_Sizes)>0 else ''
		resourceList["Brand"] = List_Brands[0] if len(List_Brands)>0 else ''

		data.append(resourceList)
	res = {
		"status":1,
		"message":"All view resources",
		"data":data,
		"total":len(data)
	}

	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/v_list.html",**commonData,**res,title=gettext('Category'))

@bp.route("/v-grid")
def v_grid():
	commonData = commonUsedData()
	return render_template ("commerce/main/commerce/v_grid.html",**commonData,title=gettext('Category'))



























# ############ tests ############

# @bp.route("/list_view")
# def list_view():
# 	resources = Resource.query.order_by(Resource.CreatedDate.desc())
# 	commonData = commonUsedData()
# 	resData = realResRelatedData()
# 	return render_template ("commerce/main/commerce/list_view.html",
# 		resources=resources,**commonData,**resData,title=gettext('Category'))

# @bp.route("/grid_view")
# def grid_view():
# 	resources = Resource.query.order_by(Resource.CreatedDate.desc())
# 	commonData = commonUsedData()
# 	resData = realResRelatedData()
# 	return render_template ("commerce/main/commerce/grid_view.html",
# 		resources=resources,**commonData,**resData,title=gettext('Category'))
