Example with Lomay sowda database server:

```sql
select ("DevUniqueId", "IsAllowed") from tbl_dk_device;
```

Using DevUniqueId = e4d788879fbe6635
byte to array = "ZTRkNzg4ODc5ZmJlNjYzNTplNGQ3ODg4NzlmYmU2NjM1"
auth_header: {"Authorization": "Basic ZTRkNzg4ODc5ZmJlNjYzNTplNGQ3ODg4NzlmYmU2NjM1"}

> request

```bash
curl --header "Authorization: Basic ZTRkNzg4ODc5ZmJlNjYzNTplNGQ3ODg4NzlmYmU2NjM1" --request GET https://ls.com.tm/ls/api/login/?type=device
```

> response

```json
{"device":{"AddInf1":"","AddInf2":"","AddInf3":"","AddInf4":"","AddInf5":"","AddInf6":"id=QP1A.190711.020,androidId=e4d788879fbe6635,baseOS=,release=10,brand=samsung,device=a7y18lte,display=QP1A.190711.020.A750FXXU5CUI4,manufacturer=samsung,model=SM-A750F,isPhysicalDevice=true","AllowedDate":null,"CreatedDate":"2022-01-29 08:00:04","CreatedUId":null,"DevDesc":null,"DevGuid":"ace9103d-9d83-4a72-8c0f-effb341b3c44","DevId":62,"DevName":"Dowlpack","DevUniqueId":"e4d788879fbe6635","DevVerifyDate":null,"DevVerifyKey":null,"DisallowedDate":null,"GCRecord":null,"IsAllowed":true,"ModifiedDate":"2022-01-29 08:00:04","ModifiedUId":null,"RpAccId":null,"SyncDateTime":"2022-01-29 08:00:04","UId":10},"exp":"2022-02-01 20:10:59","message":"Login success!","status":1,"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDM3MjgyNTksImlhdCI6MTY0MzcyMjI1OSwibmJmIjoxNjQzNzIyMjU5LCJEZXZJZCI6NjJ9.TXQgbs_oQiGlsq4LEcwZq5TLM0rRmbyWmgfAGc7N_uk"}
```
-------
connecting to websocket

wss://ls.com.tm/ws/1

send data:
{"token": "<auth_token>"}

responses "connected" othervise disconnects


> Client phone register request

```bash
curl --header "PhoneNumber: +99363509038" --request GET https://ls.com.tm/ls/api/register-request/?method=phone_number
```

> response

```json
{"data":{"CreatedDate":"2022-02-01 20:00:04","CreatedUId":null,"GCRecord":null,"ModifiedDate":"2022-02-01 23:17:19","ModifiedUId":null,"RegReqExpDate":"Tue, 01 Feb 2022 23:28:22 GMT","RegReqGuid":"50e258d7-d6d9-490b-97fc-116046c8c3c1","RegReqId":8,"RegReqInfo":null,"RegReqIpAddress":null,"RegReqPhoneNumber":"+99363509038","RegReqVerified":0,"RegReqVerifyCode":"","SyncDateTime":"2022-02-01 20:00:04","validator_phone_number":"Shu mumkincilik entak gurnalynmady.."},"message":"G\u00f6rkezilen telefon nomere bo\u015f SMS ugrady\u0148: <h4><div style=\"margin: 1rem 0\">\n\t\t\t\t<a href=\"sms:Shu mumkincilik entak gurnalynmady..\">\n\t\t\t\tShu mumkincilik entak gurnalynmady..</a>\n\t\t\t\t<a class=\"btn btn-success\" style=\"margin-left: 1rem\" href=\"sms:Shu mumkincilik entak gurnalynmady..\">\n\t\t\t\tIber</a>\n\t\t\t\t</div>\n\t\t\t\t</h4>\n Talaby\u0148yzy\u0148 i\u015fje\u0148 \u00fdagda\u00fd wagty 10 (minutes)","status":1,"total":1}
```


> websocket connected device receives:

```json
{
  "phone_number": "+99363509038",
  "verify_code": 103379
}
```
