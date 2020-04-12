from main_pack.users.models import Users, db
from main_pack.commerce.models import Product, db
from main_pack import db, create_app
app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

# user = Users(UName="admin", EMail="admin@post.in", UFullName="Administrator",UPass="admin123", UType=1)
# db.session.add(user)


db.session.commit()

# types:
# 1 = admin
# 2 = just user