from main_pack.models.base.models import Res_category

from main_pack import db, create_app

app = create_app()
app.app_context().push()

baseTemplate = {}
categories = Res_category.query.filter_by(ResOwnerCatId=0)
baseTemplate.update({'categories':categories})

for category in baseTemplate['categories']:
	print(category.ResCatName)

# for category in categories:
# 	print(category.ResCatId)

# if (category.ResOwnerCatId == '' or category.ResOwnerCatId == None or category.ResOwnerCatId == 0):
# 	child_status = "category"
# else:
# 	parent = Res_category.query.filter_by(ResCatId=newCategory.ResOwnerCatId).first()
# 	print("Parent Name:" + parent.ResCatName)
# 	if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None or parent.ResOwnerCatId == 0):
# 		child_status = "subcategory"
# 	else:
# 		child_status = "subcategory_child"