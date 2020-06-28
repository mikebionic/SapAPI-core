from flask import json, jsonify, request, make_response, abort
from sqlalchemy import and_
from datetime import datetime
import datetime as dt
import jwt
from functools import wraps
from main_pack.config import Config

from main_pack.api.auth import api
from main_pack.models.users.models import Users,Rp_acc
from main_pack.api.auth.utils import check_auth
from main_pack.api.users.utils import apiUsersData,apiRpAccData
def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		if not token:
			return jsonify({'message':'Token is missing!'}), 401
		try:
			data=jwt.decode(token, Config.SECRET_KEY)
			print(data)
			if data['UId']:
				current_user = Users.query\
					.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),Users.UId==data['UId']).first()
			elif data['RpAccId']:
				current_user = Rp_acc.query\
					.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),Rp_acc.RpAccId==data['RpAccId']).first()
		except:
			return jsonify({'message':'Token is invalid!'}), 401
		return f(current_user,*args,**kwargs)

	return decorated

@api.route('/login/users/',methods=['GET','POST'])
def api_login_users():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify. Missing username or password.',
			401, {'WWW-Authenticate':'basic realm'})
	user = Users.query\
		.filter(and_(Users.GCRecord=='' or Users.GCRecord==None),Users.UName==auth.username).first()
	if not user:
		return make_response('Could not verify. User does not exist.',
			401, {'WWW-Authenticate':'basic realm'})
	if check_auth('Users',auth.username,auth.password):
		token = jwt.encode({'UId':user.UId, 'exp':datetime.utcnow()+dt.timedelta(minutes=10)}, Config.SECRET_KEY)
		userData = apiUsersData(user.UId)
		return jsonify({'token':token.decode('UTF-8'),'user':userData['data']})
	return make_response('Could not verify', 401, {'WWW-Authenticate':'basic realm'})

@api.route('/login/rp-accs/',methods=['GET','POST'])
def api_login_rp_accs():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify. Missing username or password.',
			401, {'WWW-Authenticate':'basic realm'})
	rp_acc = Rp_acc.query\
		.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),Rp_acc.RpAccUName==auth.username).first()
	if not rp_acc:
		return make_response('Could not verify. User does not exist.',
			401, {'WWW-Authenticate':'basic realm'})
	if check_auth('Rp_acc',auth.username,auth.password):
		token = jwt.encode({'RpAccId':rp_acc.RpAccId, 'exp':datetime.utcnow()+dt.timedelta(minutes=10)}, Config.SECRET_KEY)
		rpAccData = apiRpAccData(rp_acc.RpAccId)
		return jsonify({'token':token.decode('UTF-8'),'rp_acc':rpAccData['data']})
	return make_response('Could not verify', 401, {'WWW-Authenticate':'basic realm'})
