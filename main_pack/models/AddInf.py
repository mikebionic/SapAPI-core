from main_pack import db


class AddInf(object):
	AddInf1 = db.Column("AddInf1",db.String(500))
	AddInf2 = db.Column("AddInf2",db.String(500))
	AddInf3 = db.Column("AddInf3",db.String(500))
	AddInf4 = db.Column("AddInf4",db.String(500))
	AddInf5 = db.Column("AddInf5",db.String(500))
	AddInf6 = db.Column("AddInf6",db.String(500))

	def to_json(self):
		return {
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
		}