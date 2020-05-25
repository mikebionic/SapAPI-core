from main_pack.models.commerce.models import Res_category

from main_pack.base.dataMethods import configureNulls

def addCategoryDict(req):
	ResOwnerCatId = req.get('ResOwnerCatId')
	ResCatName = req.get('ResCatName')
	ResCatDesc = req.get('ResCatDesc')
	ResCatIconName = req.get('ResCatIconName')
	category = {
		'ResOwnerCatId':ResOwnerCatId,
		'ResCatName':ResCatName,
		'ResCatDesc':ResCatDesc,
		'ResCatIconName':ResCatIconName
	}
	category = configureNulls(category)
	return category
