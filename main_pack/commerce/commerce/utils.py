from main_pack import db,babel,gettext,lazy_gettext
from main_pack.models.base.models import Company
from main_pack.models.commerce.models import Res_category

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


##### for realResRelatedData
from main_pack.models.commerce.models import Resource 
def realResRelatedData():
	resRelatedData = {}
	resources = Resource.query.all()
	barcodes = Barcode.query.all()
	resColors = Res_color.query.all()
	resSizes = Res_size.query.all()
	resTranslations = Res_translations.query.all()
	resUnits = Res_unit.query.all()
	resPrices = Res_price.query.all()
	resTotals = Res_total.query.all()
	resTransactions = Res_transaction.query.all()
	resDiscounts = Res_discount.query.all()

	images = Image.query.all()
	units = Unit.query.all()
	brands = Brand.query.all()
	usageStatuses = Usage_status.query.all()
	resCategories = Res_category.query.all()
	resTypes = Res_type.query.all()
	resMakers = Res_maker.query.all()
	rpAccs = Rp_acc.query.all()
	languages = Language.query.all()
	colors = Color.query.all()
	sizes = Size.query.all()
	brands = Brand.query.all()

	subcategory_children = []
	subcategory = Res_category.query.filter(Res_category.ResOwnerCatId!=0)
	for category in subcategory:
		parents = Res_category.query.filter(Res_category.ResCatId==category.ResOwnerCatId)
		for parent in parents:
			if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
				pass
			else:
				subcategory_children.append(category)

	resRelatedData = {
		# 'resources':resources,
		'barcodes':barcodes,
		'resColors':resColors,
		'resSizes':resSizes,
		'resTranslations':resTranslations,
		'resUnits':resUnits,
		'resPrices':resPrices,
		'resTotals':resTotals,
		'resTransactions':resTransactions,
		'resDiscounts':resDiscounts,

		'images':images,
		'units':units,
		'brands':brands,
		'usageStatuses':usageStatuses,
		'resCategories':resCategories,
		'resTypes':resTypes,
		'resMakers':resMakers,
		'rpAccs':rpAccs,
		'languages':languages,
		'colors':colors,
		'sizes':sizes,
		'brands':brands,
		}

	return resRelatedData