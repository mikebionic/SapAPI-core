from main_pack import db


class AddInf(object):
	AddInf1 = db.Column("AddInf1",db.String)
	AddInf2 = db.Column("AddInf2",db.String)
	AddInf3 = db.Column("AddInf3",db.String)
	AddInf4 = db.Column("AddInf4",db.String)
	AddInf5 = db.Column("AddInf5",db.String)
	AddInf6 = db.Column("AddInf6",db.String)

	def to_json_api(self):
		return {
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
		}