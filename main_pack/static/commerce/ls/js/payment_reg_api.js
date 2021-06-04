// payload = {
// 	"RegNo": "ff3f3f333",
// 	"TotalPrice": "45.3",
//	"OrderDesc": "Testing the service"
// }
const payment_req_url = `${url_prefix}/order-payment-register-request/`;
const checkout_oinv_url = `${url_prefix}/checkout-cart-v1/`;
const oinv_validation_url = `${url_prefix}/order-inv-validation/`;

function gen_Reg_no_and_open_payment(payload_data, url, type){
	var order_data = get_local_data_by_name("orderInv");
	var RegNum = order_data["orderInv"]["OInvRegNo"];
	if (RegNum){
		order_data["orderInv"]["InvStatId"] = 13;
		set_local_data_by_name("orderInv", order_data)
		checkoutOrder(order_data, checkout_oinv_url);
	}
	else {
		$.ajax({
			contentType: "application/json",
			dataType: "json",
			data: JSON.stringify(payload_data),
			type: type,
			url: url,
			success: function(response){
				if (response.status == 1){
					var RegNum = response.data;
					var order_data = get_local_data_by_name("orderInv");
					order_data["orderInv"]["InvStatId"] = 13;
					order_data["orderInv"]["OInvRegNo"] = RegNum;
					set_local_data_by_name("orderInv", order_data)
					checkoutOrder(order_data, checkout_oinv_url);
				}
				else{
					swal(title=error_title,desc=unknown_error_text,style="warning");
				}
			},
			error: function(response){
				console.log(response)
				swal(title=error_title,desc=unknown_error_text,style="warning");
			}
		})
	}
}


function checkoutOrder(payload_data,url){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(payload_data),
		type: 'POST',
		url: url,
		success: function(response){
			if(response.status == 1){
				var RegNum = response.data.OInvRegNo
				var order_data = get_local_data_by_name("orderInv");
				var order_lines = order_data["orderInv"]["OrderInvLines"]
				order_data["orderInv"] = response.data;
				order_data["orderInv"]["OrderInvLines"] = order_lines; 
				set_local_data_by_name("orderInv", order_data)
				req_payment_url_prepare(RegNum);
			}
			else{
				swal(title='',message=response.responseText,style='warning');
			}
		}
	})
}


function req_payment_url_prepare(reg_no){
	cart_totals_data = configure_cart_item_count()
	payload = {
		// "RegNo": "reg_no1113",
		"RegNo": reg_no,
		"TotalPrice": cart_totals_data["totalPrice"],
		"OrderDesc": $('.orderDesc').val()
	}
	req_payment_request(payload, payment_req_url)
}


function req_payment_request(payload, url){
	$.ajax({
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(payload),
		type: 'POST',
		url: url,
		success: function(response){
			var formUrl = response.data.formUrl;
			var order_data = get_local_data_by_name("orderInv");
			order_data["orderInv"]["OrderId"] = response.data.orderId;
			set_local_data_by_name("orderInv", order_data);
			validate_oinv_payment();
			// open_payment_window(formUrl)
		},
		error: function(response){
			console.log(response)
			swal(title=error_title,desc=unknown_error_text,style="warning");
		}
	})
}

function open_payment_window(url){

	// // example url
	// https://mpi.gov.tm/payment/merchants/online/payment_ru.html?mdOrder=ae8b6f3a-cc4d-406a-a5cd-931e1d1f124e
	
	// // changed to example
	// https://mpi.gov.tm/payment/merchants/online/errors_ru.html?error=payment.errors.order_already_processed

	var index_url = "mpi.gov.tm/payment/merchants/online/payment_ru.html?mdOrder"
	var window_properties = "width=600,height=400,resizable=yes,location=no"
	var paymentWin = window.open(url, 'Payment', window_properties)
	paymentWin.addEventListener('unload', function() {
		setTimeout(() => {
			if (paymentWin.location.href.indexOf(index_url) > 0){
				detect_url_change(paymentWin)
			}
		}, 5000);
	});
}

function detect_url_change(current_window){
	var current_location = current_window.location.href
	const win_location = setInterval(() => {
		try {
			console.log(current_window.location.href)
			if (current_window.location.href !== current_location) {
				console.log("url changed");
				clearInterval(win_location);
				// send validation request
			}
			if (!current_window.location.href){
				clearInterval(win_location)
			}
		} catch (e) {
			clearInterval(win_location);
		}
	}, 100);
}



function validate_oinv_payment(){
	var order_data = get_local_data_by_name("orderInv");
	var payload_data = order_data['orderInv']
	checkoutCart(payload_data, oinv_validation_url, "POST")
}