**Request**

> POST

http://<url>/<prefix>/v1/v-translations/

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
      "LangName": "en-US",
      "ResCatName": "Sagatlar",
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
    }
  ],
  "message": "Translation",
  "status": 1,
  "total": 1
}
```