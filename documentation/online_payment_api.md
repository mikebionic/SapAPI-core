

Online payment api workflow

# !! Uses API V1

> 1. Generate pred reg no by provided json configs
| __Route__    | __Methods__ | __Status__ | __Note__            |
| ------------ | :---------: | :--------: | ------------------- |
| /gen-reg-no/ |  **POST**   |   Active   | **@token required** |

**Request**

```json
{
	"RegNumTypeId": 9,
	"random_mode": 1,
	"RegNumTypeName": "sale_order_invoice_code (could be blank)"
}
```

**Response**

```json
res = {
	"status": 1,
	"data": "ANSSFK09381",
	"message": "Pred Reg_no generation"
}
```
[Example](./examples/reg_no_api.md)


--------------


OInvType = 13
OInvRegNo = <generatedRegNO>
<!--13 | Tölege garaşylýar | Sargyt edilende töleg geçirmek prosesini amala aşyrmaklyga başlady | В ожидании оплаты | Начал процесс оплаты при зака     | Awaiting payment-->

**to state**
online_payment_type = "halkbank" || "foreign_affairs_bank"

> 2. Checkout order invoice with new OInvTypeId

| __Route__                 | __Methods__ | __Status__ | __Note__            |
| ------------------------- | :---------: | :--------: | ------------------- |
| /checkout-sale-order-inv/ |  **POST**   |   Active   | **@token required** |

[Example](./examples/checkout_order_inv_api.md)


--------

> 3. Prepare URl for payment
 
 ```js
req_payment_url_prepare(RegNum);

payload = {
	"RegNo": reg_no,
	"TotalPrice": cart_totals_data["totalPrice"],
	"OrderDesc": $('.orderDesc').val()
}
var online_payment_type = order_data["online_payment_type"]

${payment_req_url}?online_payment_type=${online_payment_type}

```

> Request for order payment register
> This will return registered orderId and url that could be used for further payment

| __Route__                        | __Methods__ | __Status__ | __Note__            |
| -------------------------------- | :---------: | :--------: | ------------------- |
| /order-payment-register-request/ |  **POST**   |   Active   | **@token required** |

[Example](./examples/order_payment_register_request.md)


**Request**

```json
{
	"OInvRegNo": "OInvRegNo",
	"TotalPrice": 17.50,
	"OrderDesc": "Description text",
}
```

**Response**

```json
{
	"data": {
		"": "json data of payment registration service",
		"checkout_url": "https://....",
		"OrderId": "SomeOrderId",
		"online_payment_type": "halkbank"
	},
	"RegNo": "OInvRegNo",
	"OInvRegNo": "OInvRegNo",
	"TotalPrice": 17.50,
	"OrderDesc": "Description text
}
```

---------

> 4. Then open that returned payment url

open_payment_window(checkout_url)

```js
function open_payment_window(url){
	var window_properties = "width=600,height=400,resizable=yes,location=no"
	var paymentWin = window.open(url, 'Payment', window_properties)
	try {
		paymentWin.addEventListener('unload', function() {
			setTimeout(() => {
				detect_window_close(paymentWin);
			}, 5000);
		});
	}
	catch {
		swal(title=unknown_error_text, message=unknown_error_text, style='warning');
	}
}
```

> 5. Keep checking that payment Window closed and then do another action

```js
var payment_validated_times = 0
function detect_window_close(current_window){
	$('#cover-spin').show()
	win_closed_interval = setInterval(() => {
		try {
			if (current_window.closed){
				clearInterval(win_closed_interval);
				console.log('payment closed')
				setTimeout(() => {
					$('#cover-spin').hide()
					if (payment_validated_times < 1){
						validate_oinv_payment();
						payment_validated_times++;
					}
					else {
						clearInterval(win_closed_interval)
					}
				}, 300);
			}
		}
		catch {
			clearInterval(win_closed_interval);
		}
	}, 500);
}
```

------
> 6. Validate order inv payment


| __Route__              | __Methods__ | __Status__ | __Note__            |
| ---------------------- | :---------: | :--------: | ------------------- |
| /order-inv-validation/ |  **POST**   |   Active   | **@token required** |

[Example](./examples/order_inv_validation.md)

**Request**

```json
{
	"OrderId": "orderId of registered online service",
	"OInvRegNo": "RegNo",
	"online_payment_type": "halkbank",
	"RpAccGuid": "GUID of rp_acc if not validating as rp_acc",
}
```

**Response**

Response contains order inv data and info about validation state.

```json
{
	"data": {
		"": "response json of validation service"
	},
	"status": 1,
	"message": "Validation success"
}
```

If status == 1 
clear cart and mark checkout as done, because api does every info stated change by itself

---