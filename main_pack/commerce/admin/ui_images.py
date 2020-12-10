from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response,abort
from main_pack import db,babel,gettext
from main_pack.config import Config

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from main_pack.commerce.admin import bp

from main_pack.commerce.admin.utils import addImageDict
from main_pack.models.base.models import Image
from main_pack.base.imageMethods import allowed_image
import os, secrets
import uuid
from flask import current_app
from PIL import Image as ImageOperation

def save_picture(form_picture, path):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/'+path, picture_fn)
	form_picture.save(picture_path)
	output_size = (600,600)
	i = ImageOperation.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return {"fileName": picture_fn,"filePath": picture_path}

@bp.route('/ui/uploadImages/',methods=['POST'])
@login_required
@ui_admin_required()
def ui_uploadImages():
	if 'files[]' not in request.files:
		resp = jsonify({"message": "No file part in the request"})
		resp.status_code = 400
		return resp

	files = request.files.getlist('files[]')
	uploadedFiles=[]
	response = {}
	success = False
	for file in files:
		if file and allowed_image(file.filename):
			image = save_picture(file,"commerce/uploads")
			filename = image['fileName']
			filepath = image['filePath']
			uploadedFiles.append({
				"fileName": filename,
				"htmlData": render_template(f"{Config.COMMERCE_ADMIN_TEMPLATES_FOLDER_PATH}/imageAppend.html",
					filename=filename,filepath=filepath),
			})
			success=True
		else:
			response[file.filename] = 'File type is not allowed'
	response['files']=uploadedFiles
	if success and response:
		response['message'] = 'File(s) successfully uploaded'
		resp = jsonify(response)
		resp.status_code = 201
		return resp
	if success:
		resp = jsonify({"message": "Files successfully uploaded"})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(response)
		resp.status_code = 400
		return resp

@bp.route('/ui/images/',methods=['POST','DELETE'])
@login_required
@ui_admin_required()
def ui_images():
	if request.method == 'POST':
		req = request.get_json()
		responses=[]
		try:
			for imgReq in req:
				image = addImageDict(imgReq)
				imgId = imgReq.get('imgId')
				if (imgId == '' or imgId == None):
					image["ImgGuid"] = uuid.uuid4()
					newImage = Image(**image)
					db.session.add(newImage)
					db.session.commit()
					response = {
						"imgId": newImage.ImgId,
						"fileName": newImage.FileName,
						}
					responses.append(response)
			
			fullResponse={
				"status": "created",
				"responseText": gettext('Image')+' '+gettext('successfully saved'),
				}
			fullResponse['responses']=responses
			response = fullResponse
		except Exception as ex:
			print(ex)
			response = jsonify({
				"status": "error",
				"responseText": gettext('Unknown error!'),
				})

	if request.method == 'DELETE':
		req = request.get_json()
		imgId = req.get('imgId')
		thisImage = Image.query.get(imgId)
		thisImage.GCRecord == 1
		response = jsonify({
			"imgId": thisImage.ImgId,
			"status": "deleted",
			"responseText": gettext('Image')+' '+gettext('successfully deleted')
		})
	return response
