// payload = {
// 	"RegNo": "ff3f3f333",
// 	"TotalPrice": "45.3",
// 	"OrderDesc": "Testing the service"
// }
const payment_req_url = '127.0.0.1:5000/ls/api/order-payment-register-request/'
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
				open_payment_window(RegNum);
			}
		},
		error: function(response){
			console.log(response)
		}
	})
}

function open_payment_window(reg_no){
	payload = {
		"RegNo": reg_no,
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
			console.log(response.responseText)
			console.log(response.formUrl)
			console.log(response.orderId)
			var formUrl = response.formUrl
			var orderId = response.orderId
			open_payment_window(formUrl)
		},
		error: function(response){
			console.log(response)
		}
	})
}

function open_payment_window(url){
	var window_properties = "width=600,height=400,resizable=yes,location=no"
	var newWin = window.open(url, 'Payment', window_properties)
	newWin.addEventListener('unload', function() {
		console.log('Navigation occuring');
		console.log("loaded")
		console.log(newWin.location.href)
		console.log(newWin.location.innerText)
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
