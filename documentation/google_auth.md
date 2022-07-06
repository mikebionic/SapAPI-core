Google Login with Sap Api

> POST 

<prefix>/api/google-auth/?type=[user or rp_acc]

**payload**
```json
{
	"email": "googleData.profileObj.email",
	"username": "googleData.profileObj.givenName",
	"fullName": "googleData.profileObj.name",
	"firstName": "googleData.profileObj.givenName",
	"lastName": "googleData.profileObj.familyName",
	"imageUrl": "googleData.profileObj.imageUrl",
	"googleId": "googleData.profileObj.googleId",
	"tokenId": "googleData.tokenId",
	"accessToken": "googleData.accessToken",
}
```
-------

# Verify token (Python backend)

> https://www.googleapis.com/oauth2/v3/userinfo?access_token=<token>

```json
{
  "sub": "109052108021181693896",
  "name": "Muhammed Jepbarov",
  "given_name": "Muhammed",
  "family_name": "Jepbarov",
  "picture": "https://lh3.googleusercontent.com/a-/AOh14GilCzCzMKH0-k4MOXNGRkpzI7J58lI_lWvWxeWPLA\u003ds96-c",
  "email": "muhammedjepbarov@gmail.com",
  "email_verified": true,
  "locale": "ru"
}
```

> https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=<token>

```json
{
  "azp": "625161355157-fi9610hq69lo6g7rd6bn33tgmkjngdb7.apps.googleusercontent.com",
  "aud": "625161355157-fi9610hq69lo6g7rd6bn33tgmkjngdb7.apps.googleusercontent.com",
  "sub": "109052108021181693896",
  "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
  "exp": "1650063142",
  "expires_in": "3360",
  "email": "muhammedjepbarov@gmail.com",
  "email_verified": "true",
  "access_type": "online"
}
```

**error**
```json
{
  "error_description": "Invalid Value"
}
```


------