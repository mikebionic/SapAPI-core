from main_pack import db,babel,gettext,lazy_gettext
from main_pack.models.base.models import Res_category,Company

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