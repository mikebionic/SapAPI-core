// payload = {
// 	"RegNo": "ff3f3f333",
// 	"TotalPrice": "45.3",
// 	"OrderDesc": "Testing the service"
// }
const payment_req_url = 'ls/api/order-payment-register-request/'
function gen_Reg_no_and_open_payment(payload_data, url, type){
	$.ajax({
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(payload_data),
		type: type,
		url: url,
		success: function(response){
			if (response.status == 1){
				var RegNum = response.data;
				req_payment_url_prepare(RegNum);
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

function req_payment_url_prepare(reg_no){
	payload = {
		"RegNo": "reg_no1113",
		"TotalPrice": $('.cartTotalPrice').val(),
		"OrderDesc": $('.orderDesc').val()
	}
	console.log(payload)
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
			console.log(response)
			console.log(response.data.responseText)
			console.log(response.data.formUrl)
			console.log(response.data.orderId)
			var formUrl = response.data.formUrl
			var orderId = response.data.orderId
			open_payment_window(formUrl)
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
	
	
	var window_properties = "width=600,height=400,resizable=yes,location=no"
	var paymentWin = window.open(url, 'Payment', window_properties)
	paymentWin.addEventListener('unload', function() {
		console.log('Navigation occuring');
		console.log("loaded")
		console.log(paymentWin.location.href)
		console.log(paymentWin.location.innerText)
	});
}


// const win_location = setInterval(() => {
// 	try {
// 		console.log(newWin.location.href)
// 		if (newWin.location.origin === '/') {
// 			clearInterval(win_location);
// 		}
// 		if (!newWin.location.href){
// 			console.log("errrrrrrr")
// 			clearInterval(win_location)
// 		}
// 	} catch (e) {
// 		console.log('error occured');
// 		clearInterval(win_location);
// 	}
// }, 100);
