
$('#sms_register_form').submit(function(e){
	e.preventDefault()
	var phone_number = $('#phone-number').val()
	send_sms_register_request(phone_number)
})

function send_sms_register_request(phone_number){
	$.ajax({
		headers: {"PhoneNumber": phone_number},
		url: `${url_prefix}/request-sms-register/`,
		success: function(response){
			if (response.status == 1){
				success_toaster(message = `${success_title}: ${phone_number}`)
			}
		},
		error: function(){
			errorToaster(message = `${unknown_error_text}: ${phone_number}`);
		}
	})
}