Translation Api

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


-----
Res_translation API


> POST

http://<url>/<prefix>/v1/v-translations/

**request**

```json
[
	{
		"ResName": "Haryt",
		"ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
		"ResName": "Bi Mand Watches",
		"ResDesc": "New updated watches",
		"LangName": "en"		
	},
	{
		"ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
		"ResName": "Bi mand taze sagatlar!",
		"ResDesc": "Taze we dowrebap sagatlar",
		"LangName": "tk"		
	},
	{
		"ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
		"ResName": "часы Bi mand!",
		"ResDesc": "Современные часы с новым функционалом",
		"LangName": "ru"		
	}
]
```

**response**

```json
{
  "data": [
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 3,
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "New updated watches",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "Bi Mand Watches",
      "ResTranslGuid": "ae1b75e8-9f2a-47d2-94a0-7b87ab1d839f",
      "ResTranslId": 4,
      "SyncDateTime": "2022-03-31 16:24:52"
    },
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 1,
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "Taze we dowrebap sagatlar",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "Bi mand taze sagatlar!",
      "ResTranslGuid": "36a9ce5b-7af8-459d-8f91-952967f48452",
      "ResTranslId": 5,
      "SyncDateTime": "2022-03-31 16:24:52"
    },
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 2,
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "Современные часы с новым функционалом",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "часы Bi mand!",
      "ResTranslGuid": "2d9be9c2-43c0-47a0-86b6-021fb21975c1",
      "ResTranslId": 6,
      "SyncDateTime": "2022-03-31 16:24:52"
    }
  ],
  "fail_total": 0,
  "fails": [],
  "message": "Success",
  "status": 1,
  "success_total": 3
}
```