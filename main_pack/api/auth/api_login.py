from flask import json, jsonify, request, make_response, abort
from datetime import datetime
import datetime as dt
import jwt
from functools import wraps
from main_pack.config import Config

from main_pack.api.auth import api
from main_pack.models.users.models import Users
from main_pack.api.auth.utils import check_auth

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
			current_user = Users.query.filter_by(UId=data['UId']).first()
		except:
			return jsonify({'message':'Token is invalid!'}), 401
		return f(current_user,*args,**kwargs)

	return decorated

@api.route('/login/',methods=['GET','POST'])
def api_login():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify. Missing username or password.',
			401, {'WWW-Authenticate':'basic realm'})
	user = Users.query.filter_by(UName=auth.username).first()
	if not user:
		return make_response('Could not verify. User does not exist.',
			401, {'WWW-Authenticate':'basic realm'})
	if check_auth(auth.username,auth.password):
		token = jwt.encode({'UId':user.UId, 'exp':datetime.utcnow()+dt.timedelta(minutes=10)}, Config.SECRET_KEY)
		return jsonify({'token':token.decode('UTF-8'),'user':user.to_json_api()})
	return make_response('Could not verify', 401, {'WWW-Authenticate':'basic realm'})
