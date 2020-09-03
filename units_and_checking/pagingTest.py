pagination = [
	{
		"page": 2,
		"status": "active",
		"url": "someplace"
	},
	{
		"page": 3,
		"status": None,
		"url": "someplace"
	}
]

for page in pagination:
	if page["status"] == "active":
		print('{} - activePage'.format(page["page"]))
	if page["status"] is None:
		print('{} - disable'.format(page["page"]))