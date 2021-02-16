from cryptography.fernet import Fernet, InvalidToken


def encrypt_data(data, server_key, db_guid, client_key):
	try:
		f = Fernet(server_key)
		enc = f.encrypt(str(data).encode()).decode()
		more = f"{str(db_guid)}{enc}{str(client_key)[::-1]}".encode()
		enc = f.encrypt(more)
		return enc.decode()

	except InvalidToken as ex:
		return None


def decrypt_data(data, server_key, db_guid, client_key):
	try:
		f = Fernet(server_key)
		dec = f.decrypt(data.encode()).decode()
		dec = dec.replace(str(db_guid), '')
		dec = dec.replace(str(client_key)[::-1], '')
		dec = f.decrypt(str(dec).encode())
		return dec.decode()

	except InvalidToken as ex:
		return None