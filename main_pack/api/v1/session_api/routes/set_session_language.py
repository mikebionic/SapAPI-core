from flask import (
	jsonify,
	session,
)

from main_pack.api.v1.session_api import api

@api.route('/set-session-language/<language_code>/')
def set_session_language(language_code):
	session['language'] = language_code
	
	res = {
		"status": 1,
		"data": session['language'],
		"message": "Session language",
	}
	return jsonify(res), 200