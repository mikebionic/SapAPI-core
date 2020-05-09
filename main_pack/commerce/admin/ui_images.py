from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import addImageDict

from main_pack.models.base.models import Image

import os
import urllib.request
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))

# where to place this config in blueprints???
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/ui/images/',methods=['POST'])
def ui_images():
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	
	files = request.files.getlist('files[]')
	print(files)
	uploadedFiles=[]
	response = {}
	success = False

	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			updir = os.path.join(basedir, '../../static/commerce/uploads/')
			file.save(os.path.join(updir, filename))
			success = True
			print("it's in for loop "+file.filename)
			uploadedFiles.append({
				'fileName':file.filename,
				'htmlData':render_template('/commerce/admin/imageAppend.html',
					filename=file.filename,filepath=updir+file.filename),
			})
		else:
			response[file.filename] = 'File type is not allowed'
	response['files']=uploadedFiles
	if success and response:
		response['message'] = 'File(s) successfully uploaded'
		resp = jsonify(response)
		print(resp)
		resp.status_code = 206
		return resp
	if success:
		resp = jsonify({'message' : 'Files successfully uploaded'})
		print(resp)
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(response)
		resp.status_code = 400
		return resp

###############################
# @bp.route('/ui/res_translations/', methods=['GET','POST','PUT'])
# def ui_res_translations():
# 	languages = Language.query.all()
# 	baseTemplate = {
# 		'languages':languages,
# 		}
# 	if request.method == 'POST':
# 		req = request.get_json()
# 		resTrans = addResTransDict(req)
# 		print(resTrans)
# 		resTransId = req.get('resTransId')
# 		if (resTransId == '' or resTransId == None):
# 			newTranslation = Res_translations(**resTrans)
# 			db.session.add(newTranslation)
# 			print(newTranslation)
# 			db.session.commit()
# 			response = jsonify({
# 				'resTransId':newTranslation.ResTransId,
# 				'status':'created',
# 				'responseText':gettext('Translation')+' '+gettext('successfully saved'),
# 				'htmlData': render_template('/commerce/admin/resTransAppend.html',**baseTemplate,resTrans=newTranslation)
# 				})
# 			print(response)
# 		else:
# 			try:
# 				updateTranslation = Res_translations.query.get(int(resTransId))
# 				updateTranslation.update(**resTrans)
# 				updateTranslation.modifiedInfo(UId=current_user.UId)
# 				db.session.commit()
# 				response = jsonify({
# 						'resTransId':updateTranslation.ResTransId,
# 						'status':'updated',
# 						'responseText':gettext('Translation')+' '+gettext('successfully updated'),
# 						'htmlData': render_template('/commerce/admin/resTransAppend.html',**baseTemplate,resTrans=updateTranslation)
# 					})
# 			except:
# 				response = jsonify({
# 					'status':'error',
# 					'responseText':gettext('Unknown error!'),
# 					})
# 	if request.method == 'DELETE':
# 		req = request.get_json()
# 		resTransId = req.get('resTransId')
# 		thisTranslation = Res_translations.query.get(resTransId)
# 		thisTranslation.GCRecord == 1
# 		response = jsonify({
# 			'resTransId':thisTranslation.ResTransId,
# 			'status':'deleted',
# 			'responseText':gettext('Translation')+' '+gettext('successfully deleted')
# 		})
# 	return response


#####################################


# @app.route('/uploadajax', methods=['POST'])
# def upldfile():
# 	if request.method == 'POST':
# 		files = request.files['file']
# 		if files and allowed_file(files.filename):
# 			filename = secure_filename(files.filename)
# 			app.logger.info('FileName: ' + filename)
# 			updir = os.path.join(basedir, '/main_pack/static/commerce/uploads/')
# 			files.save(os.path.join(updir, filename))
# 			file_size = os.path.getsize(os.path.join(updir, filename))
# 			return jsonify(name=filename, size=file_size)