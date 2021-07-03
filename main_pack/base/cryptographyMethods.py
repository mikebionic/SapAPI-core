from cryptography.fernet import Fernet, InvalidToken


def encrypt_data(data, server_key, db_guid, client_key):
	try:
		if not data:
			raise Exception

		# TODO: make server key to use Config.AppWebKey, update RpAccWebKey 
		# TODO: before inserting to db or any return actions, generate fernet key
		# and encrypt it with app key with bcrypt or jwt, then save to db
		# TODO: check that any other generated fernet keys cant decrypt others
		f = Fernet(server_key)
		enc = f.encrypt(str(data).encode()).decode()
		more = f"{str(db_guid)}{enc}{str(client_key)[::-1]}".encode()
		enc = f.encrypt(more)
		return enc.decode()

	except Exception:
		return None


def decrypt_data(data, server_key, db_guid, client_key):
	try:
		if not data:
			raise Exception

		f = Fernet(server_key)
		dec = f.decrypt(data.encode()).decode()
		# TODO: add validator of existence of both guid and client key
		dec = dec.replace(str(db_guid), '')
		dec = dec.replace(str(client_key)[::-1], '')
		dec = f.decrypt(str(dec).encode())
		return dec.decode()

	except Exception:
		return None