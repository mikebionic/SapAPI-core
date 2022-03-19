**Request**

```url
http://<url>/<prefix>/v1/tbl-media/?author=Author
```

**Response**
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
      "CreatedDate": "2021-06-11 16:28:18",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": null,
      "MediaAuthor": "Author",
			"MediaBody": "...",
			"MediaCatId": null,
      "MediaDate": "2021v-translations-06-11 16:28:24",
      "MediaDesc": "Article from Author",
      "MediaGuid": "81f1a774-85b3-4fcb-ab46-94a84e990dfd",
      "MediaId": 1,
      "MediaIsFeatured": false,
      "MediaName": "Article",
      "MediaTitle": "Title",
      "MediaUrl": "https://url.com/blog/...",
      "ModifiedDate": "2021-06-11 16:28:18",
      "ModifiedUId": null,
      "SyncDateTime": "2021-06-11 16:28:18"
    }
  ],
  "message": "Media",
  "status": 1,
  "total": 1
}
```

---

> POST

http://<url>/<prefix>/v1/tbl-media/

```json
{
  "LangId": "LangId",
  "MediaCatId": "MediaCatId",
  "TagId": "TagId",
  "MediaGuid": "MediaGuid",
  "IsHidden": "IsHidden",
  "MediaName": "MediaName",
  "MediaTitle": "MediaTitle",
  "MediaDesc": "MediaDesc",
  "MediaBody": "MediaBody",
  "MediaAuthor": "MediaAuthor",
  "MediaUrl": "MediaUrl",
  "MediaDate": "MediaDate",
  "MediaIsFeatured": "MediaIsFeatured",
  "MediaViewCnt": "MediaViewCnt",
  "LangName": "LangName"
}
```

**Response**

```json
{
  "data": [
    {
      "LangId": "LangId",
      "MediaCatId": "MediaCatId",
      "TagId": "TagId",
      "MediaGuid": "MediaGuid",
      "IsHidden": "IsHidden",
      "MediaName": "MediaName",
      "MediaTitle": "MediaTitle",
      "MediaDesc": "MediaDesc",
      "MediaBody": "MediaBody",
      "MediaAuthor": "MediaAuthor",
      "MediaUrl": "MediaUrl",
      "MediaDate": "MediaDate",
      "MediaIsFeatured": "MediaIsFeatured",
      "MediaViewCnt": "MediaViewCnt"
    }
  ],
  "fail_total": 0,
  "fails": [],
  "message": "Success",
  "status": 1,
  "success_total": 1
}
```