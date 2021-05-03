from flask import (
	jsonify,
	session,
)

from main_pack.api.v1.session_api import api

@api.route('/set-session-language/<language>/')
def set_session_language(language):
	session['language'] = language
	
	res = {
		"status": 1,
		"data": session['language'],
		"message": "Session language",
	}
	return jsonify(res), 200