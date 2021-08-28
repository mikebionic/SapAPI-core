# -*- coding: utf-8 -*-
from flask import session, flash, abort, request
from datetime import datetime, timedelta
from functools import wraps

from main_pack.config import Config

def attempt_counter(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		if request.method == 'POST':

			clear_attempt_data = {
				"count": 5,
				"date": datetime.now()
			}

			if "attempt" not in session:
				session["attempt"] = clear_attempt_data.copy()

			attempt_data = session.get('attempt')
			if (attempt_data["count"] > 0):
				attempt_data["count"] -= 1
				attempt_data["date"] = datetime.now()

				if attempt_data["count"] == 1:
					flash("Last attempt for password", "warning")

			else:
				if datetime.now() > attempt_data["date"] + timedelta(minutes = Config.ATTEMPT_ERROR_TIMEOUT_MINUTES):
					session["attempt"] = clear_attempt_data.copy()

				else:
					flash("Access denied.. Please, contact administrators and try again later.", "danger")
					abort(401)

		return f(*args,**kwargs)

	return decorated