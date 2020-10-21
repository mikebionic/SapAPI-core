
# API authentication
Provide **username** and **password** in Authentication headers
+ /api/login/users/
+ /api/login/rp-accs/

# API config information
> GET

+ /api/api-config/

# Company and Division information
> GET

+ /api/company-info/

# Simple data queries and insertions
> GET POST

**@sha_required** of **Synchronizer**
+ /api/company/?CName=<CName>&CKey=<CKey>
+ /api/division/?DivName=<DivName>&DivKey=<DivKey>
+ /api/tbl-dk-barcodes/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-res-prices/
+ /api/tbl-dk-res-totals/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-images/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-rp-acc-trans-totals/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-total-transactions/
+ /api/tbl-dk-warehouses/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-work-periods/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>


# Order invoice api
> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-order-invoices/?startDate=<datetime>&endDate=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-order-invoices/<OInvRegNo>/
+ /api/tbl-dk-order-inv-lines/?DivId=<id>&notDivId=<id>
+ /api/tbl-dk-order-inv-types/

> GET 

## Filtering order invoices and invoices by datetime

**@sha_required** of **Synchronizer**

+ /api/tbl-dk-order-invoices/?startDate=<datetime>&endDate=<datetime>
+ /api/tbl-dk-invoices/?startDate=<datetime>&endDate=<datetime>

returns **all orders** if **blank**

(Provide **startDate** and **endDate**)
> **example request**
```url
/api/tbl-dk-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
```
> POST 

**@token_required** of **Rp_acc** login
+ /api/checkout-sale-order-inv/

+ /api/gen-reg-no/
```python
# example JSON for gen-reg-no
{
	"RegNumTypeId": 3,
	"random_mode": 1
}

# this will create a special RegNum and save in Pred_regnum
```

+ /api/validate-order-inv-payment/
```python
# example of request to change the Order status
{
  "OInvRegNo": "ARSFFK43013",
  "ReqStr":"language=ru&orderId=934d3b94-b95e-45ea-ad2b-a114db47a411&password=e235erHw4784fwf&userName=103122512345"
}

# url_request: https://mpi.gov.tm/payment/rest/getOrderStatus.do?language=ru&orderId=934d3b94-b95e-45ea-ad2b-a114db47a411&password=e235erHw4784fwf&userName=103122512345

# output of the url_request will be like:
{
	"expiration": "206004",
	"cardholderName": "John Doe",
	"depositAmount": 123,
	"currency": "934",
	"approvalCode": "7****9",
	"authCode": 2,
	"ErrorCode": "0",
	"ErrorMessage": "Успешно",
	"OrderStatus": 2,
	"OrderNumber": "011**0******1",
	"Pan": "99*******51",
	"Amount": 123,
	"Ip": "***.***.***.***",
	"SvfeResponse": "0"
}
# OrderStatus == 2 means "Payment success"
# URL, Key and Value should be set in Config and .env
```


> GET

## Payment info from database
+ /api/tbl-dk-payment-methods/
+ /api/tbl-dk-payment-types/

> GET 

## Get all orders of a logged Rp_acc
**@token_required** of **Rp_acc** login
+ /api/v-order-invoices/?startDate=<datetime>&endDate=<datetime>
+ /api/v-order-invoices/paginate/?page=&endDate=&invStatus=&per_page=&sort=&invoices_only=
+ /api/v-invoices/?startDate=<datetime>&endDate=<datetime>

example:
	/api/v-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948


## Get all order lines of a specific OInvRegNo if it's owner is Rp_acc
> GET 

**@token_required** of **Rp_acc** login

Returns only if the **Rp_acc** is the **owner** of invoice
+ /api/v-order-invoices/<str:OInvRegNo>/


# Resource category api
> GET POST

+ /api/tbl-dk-categories/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>

> GET

+ /api/tbl-dk-categories/<int:ResCatId>/

> GET

+ /api/tbl-dk-categories/paginate/

# Resource api
> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-resources/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>

> GET

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-resources/<int:ResId>/

## client view resource

> GET

+ /api/v-resources/?DivId=<id>&notDivId=<id>
+ /api/v-full-resources/?DivId=<id>&notDivId=<id>
+ /api/v-resources/<int:ResId>/
+ /api/tbl-dk-categories/<int:ResCatId>/v-resources/?DivId=<id>&notDivId=<id>
+ /api/v-resources/search/?tag=<BarcodeVal or ResName>&DivId=<id>&notDivId=<id>

> GET

from latest to first (needs configurations for datetime order
<!-- + /api/v-resources/paginate/?offset=<lastId>&limit=<quantity> -->
+ /api/v-resources/paginate/?filtering=&category=&brand=&per_page=&page=
+ /api/v-resources/search/?tag=

> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-rp-accs/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-users/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>

> GET

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-rp-accs/<int:RpAccRegNo>/
+ /api/tbl-dk-users/<int:UId>/
+ /api/tbl-dk-sliders/?DivId=<id>&notDivId=<id>