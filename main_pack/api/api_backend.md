Api backend Web Service calls.
____________________________________

# Categories and Res_category table

# Get all categories in one go
GET: /api/categories/

## Output:
``` JSON
{
	"status": "success",
	"message": "Category added",
	"data":{
		"categories":[{},{},{}],
	}
}
```
----------------------------------

# Create categories by sending a list of categories
POST: /api/categories/
``` JSON
{
	"categories":[
		{
			"ResOwnerCatId":0,
			"ResCatName":"Test1",
			"ResCatDesc":"Dectription for Test1"
		},
		{
			"ResOwnerCatId":2,
			"ResCatName":"Test2",
			"ResCatDesc":"Dectription for Test2"
		},
		{
			"ResOwnerCatId":5,
			"ResCatName":"Test3"
		}
	]
}
````
## Output:
``` JSON
{
    "data": {
        "categories": [
            {
                "ResCatDesc": "Dectription for Test1",
                "ResCatIconName": null,
                "ResCatName": "Test1",
                "ResOwnerCatId": 0
            },
            {
                "ResCatDesc": "Dectription for Test2",
                "ResCatIconName": null,
                "ResCatName": "Test2",
                "ResOwnerCatId": 2
            },
            {
                "ResCatDesc": null,
                "ResCatIconName": null,
                "ResCatName": "Test3",
                "ResOwnerCatId": 5
            }
        ]
    },
    "message": "Categories added",
    "status": "success"
}
```
--------------------------------

# Update categories by sending a list of updated categories (ResCatId required)
PUT: /api/categories/
```JSON
{
	"categories":[
		{
			"ResCatId":4,
			"ResOwnerCatId":0,
			"ResCatName":"Wow test1",
			"ResCatDesc":"Better decription for Test1"
		},
		{
			"ResCatId":65,
			"ResOwnerCatId":2,
			"ResCatName":"UPdate Test 2",
			"ResCatDesc":"New Description"
		}
	]
}
```
## Output:
```JSON
{
    "data": {
        "categories": [
            {
                "ResCatDesc": "Better decription for Test1",
                "ResCatIconName": null,
                "ResCatId": 4,
                "ResCatName": "Wow test1",
                "ResOwnerCatId": 0
            },
            {
                "ResCatDesc": "New Description",
                "ResCatIconName": null,
                "ResCatId": 65,
                "ResCatName": "UPdate Test 2",
                "ResOwnerCatId": 2
            }
        ]
    },
    "message": "Categories updated",
    "status": "success"
}
```
_______________________________________________

# Resources and Resource table

# Get all resources in one go
GET: /api/resources/

# Add new resources
POST: /api/resources/

```JSON
{
	"resources":[
		{
			"CId":1,
			"DivId":1,
			"ResCatId":3,
			"UnitId":1,
			"BrandId":null,
			"UsageStatusId":1,
			"ResTypeId":1,
			"ResMainImgId":null,
			"ResMakerId":null,
			"ResLastVendorId":null,
			"ResRegNo":"DKHK45",
			"ResName":"Owadan Kartoshka",
			"ResDesc":"Oran bet we yokary hili Kartoshka",
			"ResFullDesc":null,
			"ResWidth":null,
			"ResHeight":null,
			"ResLength":null,
			"ResWeight":null,
			"ResProductionOnSale":null,
			"ResMinSaleAmount":null,
			"ResMaxSaleAmount":null,
			"ResMinSalePrice":null,
			"ResMaxSalePrice":null
		}
	]
}
```
## Output:
```JSON
{
    "data": {
        "resources": [
            {
                "BrandId": null,
                "CId": 1,
                "DivId": 1,
                "ResCatId": 3,
                "ResDesc": "Oran bet we yokary hili Kartoshka",
                "ResFullDesc": null,
                "ResHeight": 0,
                "ResId": null,
                "ResLastVendorId": null,
                "ResLength": 0,
                "ResMainImgId": null,
                "ResMakerId": null,
                "ResMaxSaleAmount": 0,
                "ResMaxSalePrice": 0,
                "ResMinSaleAmount": 0,
                "ResMinSalePrice": 0,
                "ResName": "Owadan Kartoshka",
                "ResProductionOnSale": false,
                "ResRegNo": "DKHK45",
                "ResTypeId": 1,
                "ResWeight": 0,
                "ResWidth": 0,
                "UnitId": 1,
                "UsageStatusId": 1
            }
        ]
    },
    "message": "Resources added",
    "status": "success"
}
```