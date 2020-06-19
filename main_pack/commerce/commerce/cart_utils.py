# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image
###
from main_pack.models.base.models import Language
from main_pack.models.commerce.models import Color,Size,Brand
from main_pack.models.commerce.models import Resource
from main_pack.base.apiMethods import fileToURL


def UiCartResourceData(product_list):
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

	for product in product_list:
		resource = Resource.query.get(product["resId"])
		################
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
		resourceList["FilePathS"] = fileToURL(size='S',name=List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathM"] = fileToURL(size='M',name=List_FileName[0]) if len(List_FileName)>0 else ''
		resourceList["FilePathR"] = fileToURL(size='R',name=List_FileName[0]) if len(List_FileName)>0 else ''

		# configure this for uniqueness later on
		imagesList = []
		for imageName in List_FileName:
			resImage = {}
			resImage["FilePathS"] = fileToURL(size='S',name=imageName) if len(List_FileName)>0 else ''
			resImage["FilePathM"] = fileToURL(size='M',name=imageName) if len(List_FileName)>0 else ''
			resImage["FilePathR"] = fileToURL(size='R',name=imageName) if len(List_FileName)>0 else ''
			imagesList.append(resImage)
		resourceList['Images'] = imagesList

		resourceList["Colors"] = List_Colors if len(List_Colors)>0 else ''
		resourceList["Sizes"] = List_Sizes if len(List_Sizes)>0 else ''
		resourceList["Brand"] = List_Brands[0] if len(List_Brands)>0 else ''

		try:
			resourceList["productQty"] = product["productQty"]
		except:
			resourceList["productQty"] = 1
		data.append(resourceList)
	#############
	res = {
		"status":1,
		"data":data,
		"total":len(data)
	}
	return res