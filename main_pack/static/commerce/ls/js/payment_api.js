

gen_reg_no_data = {
	"RegNumTypeName": "sale_order_invoice_code",
	"random_mode": 1,
}


function service_post(payload_data, url, type){
	$.ajax({
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(payload_data),
		type: type,
		url: url,
		success: function(response){
			if (response.status == 1){
				var RegNum = response.data;
				open_payment_window(reg_no = RegNum);
			}
		},
		error: function(response){
			console.log(response)
		}
	})
}

function req_payment_url_info(url){
	$.ajax({
		type: 'GET',
		headers: {
			"Access-Control-Allow-Origin": "*",
    },
		url: url,
		success: function(response){
			console.log(response)
			console.log(response.responseText)
			// var res = response.data;
		},
		error: function(response){
			console.log(response)
		}
	})
}

function open_payment_window(reg_no){
	var url = "https://mpi.gov.tm/payment/rest/register.do?";
	var orderNumber = reg_no;
	var amount = $('.cartTotalPrice').val() * 100;
	console.log(amount);
	var currency = 934;
	var language = "ru";
	var password = "e235erHw4784fwf";
	var orderDesc = $('.orderDesc').val();
	console.log(orderDesc);
	var returnUrl = `https://mpi.gov.tm/payment/finish.html%3Flogin%3D103122512345%26password%3De235erHw4784fwf&userName=103122512345&pageView=DESKTOP&description=${orderDesc}`


	payment_order_check_req_url = `${url}orderNumber=${orderNumber}&currency=${currency}&amount=${amount}&language=${language}&password=${password}&returnUrl=${returnUrl}`
	console.log(payment_order_check_req_url);
	req_payment_url_info(url = payment_order_check_req_url)

}

