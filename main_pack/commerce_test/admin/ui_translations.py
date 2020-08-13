from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db_test,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce_test.admin import bp

from main_pack.commerce_test.admin.utils import addResTransDict,addLanguageDict
from main_pack.models_test.commerce.models import Res_translations
from main_pack.models_test.base.models import Language


@bp.route('/ui/res_translations/', methods=['GET','POST','PUT'])
def ui_res_translations():
	languages = Language.query.all()
	baseTemplate = {
		'languages':languages,
		}
	if request.method == 'POST':
		req = request.get_json()
		resTrans = addResTransDict(req)
		print(resTrans)
		resTransId = req.get('resTransId')
		if (resTransId == '' or resTransId == None):
			newTranslation = Res_translations(**resTrans)
			db_test.session.add(newTranslation)
			print(newTranslation)
			db_test.session.commit()
			response = jsonify({
				'resTransId':newTranslation.ResTransId,
				'status':'created',
				'responseText':gettext('Translation')+' '+gettext('successfully saved'),
				'htmlData': render_template('/commerce/admin/resTransAppend.html',**baseTemplate,resTrans=newTranslation)
				})
			print(response)
		else:
			try:
				updateTranslation = Res_translations.query.get(int(resTransId))
				updateTranslation.update(**resTrans)
				updateTranslation.modifiedInfo(UId=current_user.UId)
				db_test.session.commit()
				response = jsonify({
						'resTransId':updateTranslation.ResTransId,
						'status':'updated',
						'responseText':gettext('Translation')+' '+gettext('successfully updated'),
						'htmlData': render_template('/commerce/admin/resTransAppend.html',**baseTemplate,resTrans=updateTranslation)
					})
			except Exception as ex:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	if request.method == 'DELETE':
		req = request.get_json()
		resTransId = req.get('resTransId')
		thisTranslation = Res_translations.query.get(resTransId)
		thisTranslation.GCRecord == 1
		response = jsonify({
			'resTransId':thisTranslation.ResTransId,
			'status':'deleted',
			'responseText':gettext('Translation')+' '+gettext('successfully deleted')
		})
	return response