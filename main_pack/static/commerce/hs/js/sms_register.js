var request_done = 0
$('#sms_register_form').submit(function(e){
	e.preventDefault()
	var phone_number = $('#phone-number').val()
	send_sms_register_request(phone_number)
})

function send_sms_register_request(phone_number){
	request_done++;
	if (request_done == 1){
		$.ajax({
			headers: {"PhoneNumber": phone_number},
			url: `${url_prefix}/request-sms-register/`,
			success: function(response){
				if (response.status == 1){
					request_done = true;
					swal(
						title = `${success_title}: ${phone_number}`,
						message = response.message,
						style = "success")

					var current_time = Date.now()

					validation_interval = setInterval(() => {
						if (Date.now() > current_time + 9*60000){
							clearInterval(validation_interval)
							location.reload();
						}
						check_for_phone_validation(phone_number)
					}, 5000);
				}
				else {
					swal(
						title = error_title,
						message = `${response.message}`)
				}
			},
			error: function(){
				swal(message = `${unknown_error_text}: ${phone_number}`);
			}
		})
	}
	else if (request_done > 3) {
		location.reload()
	}
}

function check_for_phone_validation(phone_number){
	$.ajax({
		headers: {"PhoneNumber": phone_number},
		url: `${url_prefix}/check-sms-register/`,
		success: function(response){
			if (response.status == 1){
				request_done = true;
				swal(
					title = `${success_title}: ${phone_number}`,
					message = response.message,
					style = "success")
				setTimeout(() => {
					location.reload();
				}, 2000);
			}
		},
		error: function(){
			errorToaster(message = `${unknown_error_text}: Couldn't validate phone number, try again later.`);
		}
	})
}
