from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
pw_hash = bcrypt.generate_password_hash('123')
print(pw_hash)


hashCheck = bcrypt.check_password_hash(pw_hash, '123')

print(hashCheck) #should return Boolean