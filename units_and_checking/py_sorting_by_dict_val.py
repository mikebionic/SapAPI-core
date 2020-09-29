Images = [
	{
		"BrandId": None, 
		"CId": None, 
		"CreatedDate": "2020-09-21 21:35:54", 
		"CreatedUId": None, 
		"EmpId": None, 
		"FileName": "11fe6f9910faa6455e71df4966ce.jpg", 
		"FilePath": "/ls/api/get-image/image/M/11fe6f9910faa6455e71df4966ce.jpg", 
		"FilePathM": "/ls/api/get-image/image/M/11fe6f9910faa6455e71df4966ce.jpg", 
		"FilePathR": "/ls/api/get-image/image/R/11fe6f9910faa6455e71df4966ce.jpg", 
		"FilePathS": "/ls/api/get-image/image/S/11fe6f9910faa6455e71df4966ce.jpg", 
		"GCRecord": None, 
		"ImgId": 1340, 
		"ModifiedDate": "2020-09-19 19:09:09", 
		"ModifiedUId": None, 
		"ResId": 7285, 
		"RpAccId": None, 
		"UId": None
	}, 
	{
		"BrandId": None, 
		"CId": None, 
		"CreatedDate": "2020-09-05 08:53:26", 
		"CreatedUId": None, 
		"EmpId": None, 
		"FileName": "9e29d06454953740909c4575259e.jpg", 
		"FilePath": "/ls/api/get-image/image/M/9e29d06454953740909c4575259e.jpg", 
		"FilePathM": "/ls/api/get-image/image/M/9e29d06454953740909c4575259e.jpg", 
		"FilePathR": "/ls/api/get-image/image/R/9e29d06454953740909c4575259e.jpg", 
		"FilePathS": "/ls/api/get-image/image/S/9e29d06454953740909c4575259e.jpg", 
		"GCRecord": None, 
		"ImgId": 1333, 
		"ModifiedDate": "2020-09-18 22:52:01", 
		"ModifiedUId": None, 
		"ResId": 7285, 
		"RpAccId": None, 
		"UId": None
	}
]

sorting_images = (sorted(Images, key = lambda i: i['ModifiedDate']))
print(sorting_images[-1])