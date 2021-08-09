from cryptography.fernet import Fernet


def encrypt_data(data, fernet_key, db_guid):
	try:
		if not data or not db_guid:
			print(f"cryptography encrypt exception: no data or guid: {str(data)}, {str(db_guid)}")
			raise Exception

		f = Fernet(fernet_key)
		enc = f.encrypt(str(data).encode()).decode()
		more = f"{str(db_guid)}{enc}{str(fernet_key)[::-1]}".encode()
		enc = f.encrypt(more)
		return enc.decode()

	except Exception:
		return None


def decrypt_data(data, fernet_key, db_guid):
	try:
		if not data or not db_guid:
			print(f"cryptography decrypt exception: no data or guid: {str(data)}, {str(db_guid)}")
			raise Exception

		f = Fernet(fernet_key)
		dec = f.decrypt(data.encode()).decode()
		dec.index(str(db_guid))
		dec = dec.replace(str(db_guid), '')
		dec.index(str(fernet_key)[::-1])
		dec = dec.replace(str(fernet_key)[::-1], '')
		dec = f.decrypt(str(dec).encode())
		return dec.decode()

	except Exception:
		return None