def get_error_type(error_type):
	fail_statuses = {
		1:"Deleted",
		2:"Usage satus: Inactive",
		3:"Resource ended",
		4:"False price"
	}
	# print(fail_statuses[error_type])
	return fail_statuses[error_type]

error = get_error_type(4)
print(error)