from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response,abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.users import bp
from main_pack.commerce.users.forms import UpdateProfileForm,UpdateRpAccForm
from main_pack.commerce.commerce.utils import UiCategoriesList

from main_pack.models.base.models import Image,Rp_acc
from main_pack.base.imageMethods import save_image

from functools import wraps
def admin_required():
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user:
				return redirect(url_for('commerce_auth.login'))
			elif not current_user.is_admin():
				flash(lazy_gettext('You do not have access to that page!'), 'danger')
				return redirect(url_for('commerce.commerce'))
			return f(*args, **kwargs)
		return decorated_function
	return decorator

@bp.route("/profile")
@login_required
def profile():
	categoryData = UiCategoriesList()
	rpAcc = Rp_acc.query.filter(Rp_acc.UId==current_user.UId).first()
	if rpAcc:
		image = Image.query.filter_by(RpAccId=rpAcc.RpAccId).order_by(Image.CreatedDate.desc()).first()
		if image:
			avatar = url_for('static', filename=image.FileName)
		else:
			avatar = url_for('static', filename="commerce/uploads/noPhoto.png") 

	return render_template ("commerce/main/users/profile.html",**categoryData,
		title=gettext('Profile'),rpAcc=rpAcc,avatar=avatar)

@bp.route("/profile_edit",methods=['GET','POST'])
@login_required
def profile_edit():
	form = UpdateRpAccForm()
	rpAcc = Rp_acc.query.filter(Rp_acc.UId==current_user.UId).first()
	
	if form.validate_on_submit():
		userData = {
			'UName':form.username.data,
			'UFullName':form.fullname.data
		}
		current_user.update(**userData)

		rpAccData = {
			'RpAccName':form.fullname.data,
			'RpAccAddress':form.address.data,
			'RpAccMobilePhoneNumber':form.mobilePhone.data,
			'RpAccHomePhoneNumber':form.homePhone.data,
			'RpAccZipCode':form.zipCode.data,
			# 'RpAccEMail':form.email.data
		}
		rpAcc.update(**rpAccData)
		print(rpAccData)
		if form.picture.data:
			imageFile = save_image(imageForm=form.picture.data,module="commerce/Rp_acc",id=rpAcc.RpAccId)
			image = Image(FileName=imageFile['FileName'],FilePathR=imageFile['FilePathR'],FilePathM=imageFile['FilePathM'],
				FilePathS=imageFile['FilePathS'],RpAccId=rpAcc.RpAccId)
			db.session.add(image)

		db.session.commit()
		flash(lazy_gettext('Profile successfully updated!'), 'success')
		return redirect(url_for('commerce_users.profile'))
	
	
	form.username.data = current_user.UName
	form.fullname.data = current_user.UFullName
	form.address.data = rpAcc.RpAccAddress
	form.mobilePhone.data = rpAcc.RpAccMobilePhoneNumber
	form.homePhone.data = rpAcc.RpAccHomePhoneNumber
	form.zipCode.data = rpAcc.RpAccZipCode

	image = Image.query.filter_by(RpAccId=rpAcc.RpAccId).order_by(Image.CreatedDate.desc()).first()
	if image:
		avatar = url_for('static', filename=image.FileName)
	else:
		avatar = url_for('static', filename="commerce/uploads/noPhoto.png") 
	
	categoryData = UiCategoriesList()
	return render_template ("commerce/main/users/profile_edit.html",**categoryData,
		title=gettext('Edit profile'),form=form,avatar=avatar)