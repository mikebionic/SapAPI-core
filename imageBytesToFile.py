from main_pack.models.base.models import Image,Rp_acc
from main_pack.base.imageMethods import save_image,dirHandler
from main_pack import db, create_app

from PIL import Image as ImageOperations
import io
import os
import base64
from sqlalchemy import or_, and_


app = create_app()
app.app_context().push()

images = Image.query.filter(and_(Image.Image!=None, Image.FileName==None)).all()


for image in images:
	imageBytes = image.Image
	if image.RpAccId:
		module = "uploads/commmerce/Rp_acc"
		id = image.RpAccId
	elif image.ResId:
		module = "uploads/commerce/Resource"
		id = image.ResId
	elif image.EmpId:
		module = "uploads/Employee"
		id = image.EmpId
	elif image.CId:
		module = "uploads/Company"
		id = image.CId
	elif image.UId:
		module = "uploads/Users"
		id = image.UId
	else:
		module = None
		id = None

	dumpFolderPath = os.path.join(app.root_path,'static/imageDumps')
	dirHandler(dumpFolderPath)
	dumpImagePath = os.path.join(dumpFolderPath,"dump.jpg")
	outfile = open(dumpImagePath,"wb")
	outfile.write(base64.decodebytes(imageBytes))
	outfile.flush()
	outfile.close()
	imageFile = save_image(savedImage=dumpImagePath,module=module,id=id)
	image.FileName = imageFile["FilePathR"]
	print(imageFile)

	db.session.commit()