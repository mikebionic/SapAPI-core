**Request**

> POST

```json
[
	{
		"TranslName": "Кофеварка",
		"LangName": "ru",
		"ResCatName": "Kofe",
		"TranslDesc": "Используются для изгтовленгя кофе"
	},
	{
		"TranslName": "Peripherals",
		"LangName": "en",
		"ResCatName": "perife",
		"TranslDesc": "a devised used for computer tah attached"
	},
	{
		"TranslName": "Watches",
		"LangName": "en",
		"ResCatName": "saga",
		"TranslDesc": "Clock devices"
	}
]
```

**Response**

```json
{
  "data": [
    {
      "LangName": "ru",
      "ResCatName": "Kofe",
      "TranslDesc": "Используются для изгтовленгя кофе",
      "TranslName": "Кофеварка"
    },
    {
      "LangName": "en",
      "ResCatName": "perife",
      "TranslDesc": "a devised used for computer tah attached",
      "TranslName": "Peripherals"
    },
    {
      "LangName": "en",
      "ResCatName": "saga",
      "TranslDesc": "Clock devices",
      "TranslName": "Watches"
    }
  ],
  "fail_total": 0,
  "fails": [],
  "message": "Success",
  "status": 1,
  "success_total": 3
}
```
---

> GET

http://<url>/<prefix>/v1/v-translations/?language=en

**Response**

```json
{
  "data": [
    {
      "AddInf1": "", 
      "AddInf2": "", 
      "AddInf3": "", 
      "AddInf4": "", 
      "AddInf5": "", 
      "AddInf6": "", 
      "ColorId": null, 
      "CreatedDate": "2022-02-10 15:08:00", 
      "CreatedUId": 0, 
      "GCRecord": null, 
      "LangId": 3, 
      "ModifiedDate": "2022-02-10 16:02:51", 
      "ModifiedUId": 0, 
      "ProdId": null, 
      "ResCatId": 3, 
      "SlImgId": null, 
      "SyncDateTime": null, 
      "TranslDesc": "Clock devices", 
      "TranslGuid": "28ab309b-402a-49a7-928c-eb687e140676", 
      "TranslId": 1, 
      "TranslName": "Watches"
    }, 
    {
      "AddInf1": "", 
      "AddInf2": "", 
      "AddInf3": "", 
      "AddInf4": "", 
      "AddInf5": "", 
      "AddInf6": "", 
      "ColorId": null, 
      "CreatedDate": "2022-02-10 15:09:42", 
      "CreatedUId": 0, 
      "GCRecord": null, 
      "LangId": 3, 
      "ModifiedDate": "2022-02-10 15:09:42", 
      "ModifiedUId": 0, 
      "ProdId": null, 
      "ResCatId": 7, 
      "SlImgId": null, 
      "SyncDateTime": null, 
      "TranslDesc": null, 
      "TranslGuid": "ea83ada2-89a2-41cc-8e0f-042779d7f7cd", 
      "TranslId": 2, 
      "TranslName": "Coolers"
    }, 
    {
      "AddInf1": null, 
      "AddInf2": null, 
      "AddInf3": null, 
      "AddInf4": null, 
      "AddInf5": null, 
      "AddInf6": null, 
      "ColorId": null, 
      "CreatedDate": "2022-02-10 15:54:22", 
      "CreatedUId": null, 
      "GCRecord": null, 
      "LangId": 3, 
      "ModifiedDate": "2022-02-10 16:02:51", 
      "ModifiedUId": null, 
      "ProdId": null, 
      "ResCatId": 1, 
      "SlImgId": null, 
      "SyncDateTime": "2022-02-10 15:54:22", 
      "TranslDesc": null, 
      "TranslGuid": "4d5e896b-0677-49a2-8e40-8d91bdf170f9", 
      "TranslId": 9, 
      "TranslName": "Smartphones"
    }, 
    {
      "AddInf1": null, 
      "AddInf2": null, 
      "AddInf3": null, 
      "AddInf4": null, 
      "AddInf5": null, 
      "AddInf6": null, 
      "ColorId": null, 
      "CreatedDate": "2022-02-10 16:02:51", 
      "CreatedUId": null, 
      "GCRecord": null, 
      "LangId": 3, 
      "ModifiedDate": "2022-02-10 16:02:51", 
      "ModifiedUId": null, 
      "ProdId": null, 
      "ResCatId": 8, 
      "SlImgId": null, 
      "SyncDateTime": "2022-02-10 16:02:51", 
      "TranslDesc": "Used to create coffee", 
      "TranslGuid": "f2d612ab-87d3-43ce-b8eb-fc7a13e546ba", 
      "TranslId": 10, 
      "TranslName": "Coffe makers"
    }, 
    {
      "AddInf1": null, 
      "AddInf2": null, 
      "AddInf3": null, 
      "AddInf4": null, 
      "AddInf5": null, 
      "AddInf6": null, 
      "ColorId": null, 
      "CreatedDate": "2022-02-10 16:02:51", 
      "CreatedUId": null, 
      "GCRecord": null, 
      "LangId": 3, 
      "ModifiedDate": "2022-02-10 16:02:51", 
      "ModifiedUId": null, 
      "ProdId": null, 
      "ResCatId": 4, 
      "SlImgId": null, 
      "SyncDateTime": "2022-02-10 16:02:51", 
      "TranslDesc": "a devised used for computer tah attached", 
      "TranslGuid": "826bf007-3f16-479d-abc7-410e8aad94ee", 
      "TranslId": 12, 
      "TranslName": "Peripherals"
    }
  ], 
  "message": "Translation", 
  "status": 1, 
  "total": 5
}
```