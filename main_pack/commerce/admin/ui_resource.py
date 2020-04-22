from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.commerce.admin.utils import addCategoryDict
from main_pack.models.base.models import Resource_category

@bp.route("/admin/category/", methods=['GET','POST','PUT','DELETE'])
def ui_category():
	categories = Resource_category.query.all()
	baseTemplate = {
		'categories':categories,
		}
	if request.method == "POST":
		try:
			req = request.get_json()
			category = addCategoryDict(req)
			newCategory = Resource_category(**category)
			db.session.add(newCategory)
			db.session.commit()
			if (newCategory.ResOwnerCatId == '' or newCategory.ResOwnerCatId == None):
				child_status = "category"
			else:
				parent = Resource_category.query.filter_by(ResOwnerCatId=newCategory.ResOwnerCatId).first()
				if (parent.ResOwnerCatId == '' or parent.ResOwnerCatId == None):
					child_status = "category_child"
				else:
					child_status = "subcategory_child"
			response = jsonify({
				'catId':newCategory.RegCatId,
				'status':'created',
				'child_status':child_status,
				'responseText':gettext('Category')+' '+gettext('successfully saved!'),
				'data':render_template('commerce/admin/appendingCategory.html',child_status=child_status,category=newCategory)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	elif request.method == "DELETE":
		req = request.get_json()
		catId = req.get('catId')
		thisCategory = Resource_category.query.get(catId)
		thisCategory.GCRecord = 1
		db.session.commit()
		response = {
			'status':'deleted',
			'responseText':thisCategory.ResCatName+' '+gettext('successfully deleted'),
		}

	return response

@bp.route('/admin/resource/colors', methods=['GET','POST','PUT'])
def resource_colors():
	schoolTypes = School_type.query.all()
	baseTemplate = {
		'schoolTypes':schoolTypes
		}
	if request.method == 'POST':
		req = request.get_json()
		school = addSchoolDict(req)
		schoolId = req.get('schoolId')
		if (schoolId == '' or schoolId == None):
			newSchool = School(**school)
			db.session.add(newSchool)
			db.session.commit()
			response = jsonify({
				'schoolId':newSchool.SchoolId,
				'status':'created',
				'responseText':gettext('School')+' '+gettext('successfully saved'),
				'data': render_template('/hr_department/tableSchoolAppend.html',**baseTemplate,school=newSchool)
				})
		else:
			try:
				updateSchool = School.query.get(int(schoolId))
				updateSchool.update(**school)
				updateSchool.modifiedInfo(UId=current_user.UId)
				db.session.commit()
				response = jsonify({
						'schoolId':updateSchool.SchoolId,
						'status':'updated',
						'responseText':gettext('School')+' '+gettext('successfully updated'),
						'data': render_template('/hr_department/tableSchoolAppend.html',**baseTemplate,school=updateSchool)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	if request.method == 'PUT':
		req = request.get_json()
		schoolId = req.get('schoolId')
		thisSchool = School.query.get(schoolId)
		response = {
			'schoolId':schoolId,
			'thisSchool':thisSchool.to_json()
		}
	return response