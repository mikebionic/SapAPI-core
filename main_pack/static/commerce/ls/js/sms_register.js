var request_done = 0
var user_register_token = null

$('#sms_register_form').submit(function(e){
	e.preventDefault()
	var phone_number = $('#phone-number').val()
	send_sms_register_request(phone_number)
})

function send_sms_register_request(phone_number){
	request_done++;
	if (request_done > 3) {
		location.reload()
	}
	else {
		$.ajax({
			headers: {"PhoneNumber": phone_number},
			url: `${api_url_prefix}/request-sms-register/`,
			success: function(response){
				console.log(responseisEmpty)
				if (response.status == 1){
					destroy_phone_request_form();
					show_loader_spinner();
					request_done = true;
					swal(
						title = `${success_title}: ${phone_number}`,
						message = response.message,
						style = "success")

					var current_time = Date.now()

					validation_interval = setInterval(() => {
						// after 9 minutes:
						if (Date.now() > current_time + 9*60000){
							clearInterval(validation_interval)
							location.reload();
						}
						check_for_phone_validation(phone_number, validation_interval)
					}, 10000);
				}
				else {
					swal(
						title = error_title,
						message = `${response.message}`,
						style = "warning")
				}
			},
			error: function(){
				swal(
					title = error_title,
					message = `${unknown_error_text}: ${phone_number}`,
					style = "error");
			}
		})
	}
}

function check_for_phone_validation(phone_number, validation_interval){
	$.ajax({
		headers: {"PhoneNumber": phone_number},
		url: `${api_url_prefix}/check-sms-register/`,
		success: function(response){
			if (response.status == 1){
				request_done = true;
				swal(
					title = `${success_title}: ${phone_number}`,
					message = response.message,
					style = "success")
				
				clearInterval(validation_interval);
				user_register_token = response.data["token"]
			
				hide_loader_spinner();
				show_user_register_form();
			}
		},
		error: function(){
			// errorToaster(message = `${unknown_error_text}: Couldn't validate phone number, try again later.`);
		}
	})
}

$('#user-register-form').submit(function(e){
	e.preventDefault();
	if (user_register_token){
		var user_data = collect_register_user_data(
			$('#username').val().trim(),
			$('#full-name').val().trim(),
			$('#address').val().trim(),
			$('#password').val().trim(),
			$('#confirm-password').val().trim(),
		);
		if (!isEmpty(user_data)){
			$.ajax({
				headers: {"token": user_register_token},
				contentType: "application/json",
				dataType: "json",
				data: JSON.stringify(user_data),
				type: "POST",
				url: `${api_url_prefix}/register/?method=phone_number&type=rp_acc`,
				success: function(response){
					if (response){
						if (response.status == 1){
							swal(
								title = success_title,
								message = response.message,
								style = "success"
							)
							setTimeout(() => {
								location.href = location.origin;
							}, 3000);
						}
					}
				},
				error: function(){
					errorToaster(message = unknown_error_text);
				}
			})
		}
	}
	else{
		swal(
			title = error_title,
			message = `${unknown_error_text} \n, Try again or contact administartiors`,
			style = "error");
		setTimeout(() => {
			location.href = location.origin;
		}, 5000);
	}
})


function collect_register_user_data(
	username,
	full_name,
	address,
	password,
	confirm_password,
){
	var data = {}
	if (password != confirm_password || password == ''){
		errorToaster("Passwords did not match!!")
		return data
	}

	data = {
		"RpAccUName": username,
		"RpAccUPass": password,
		"RpAccAddress": address,
		"RpAccName": full_name,
	}

	return data
}

function destroy_phone_request_form(){
	$('#sms_register_form').remove()
}

function show_user_register_form(){
	$('#user-register-form').show()
}

function show_loader_spinner(){
	$(`#sms-reg-spinner`).show()
}

function hide_loader_spinner(){
	$(`#sms-reg-spinner`).hide()
}