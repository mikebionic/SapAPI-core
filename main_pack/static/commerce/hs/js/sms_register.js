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
			headers: {"phone_number": phone_number},
			url: `${api_url_prefix}/request-sms-register/`,
			success: function(response){
				if (response.status == 1){
					destroy_phone_request_form();
					show_loader_spinner();
					request_done = true;
					swal(
						title = `${success_title}: ${phone_number}`,
						message = response.message,
						style = "success")

					$('.swal-text').html($('.swal-text').text())
					var current_time = Date.now()
					$('.swal-button-container').remove()

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
		headers: {"phone_number": phone_number},
		url: `${api_url_prefix}/check-sms-register/`,
		success: function(response){
			if (response.status == 1){
				request_done = true;
				swal(
					title = `${success_title}: ${phone_number}`,
					message = response.message,
					style = "success")
				
				$('.swal-text').html($('.swal-text').text())
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
			$('#password').val() ? $('#password').val().trim() : null,
			$('#confirm-password').val() ? $('#confirm-password').val().trim() : null,
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

							$('.swal-text').html($('.swal-text').text())
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


function send_sms_login_request(phone_number){
	request_done++;
	if (request_done > 3) {
		location.reload()
	}
	else {
		$.ajax({
			headers: {"phone_number": phone_number},
			url: `${api_url_prefix}/request-sms-login/`,
			success: function(response){
				if (response.status == 1){
					show_loader_spinner();
					request_done = true;
					swal(
						title = `${success_title}: ${phone_number}`,
						message = response.message,
						style = "success")

					$('.swal-text').html($('.swal-text').text())
					var current_time = Date.now()

					validation_interval = setInterval(() => {
						// after 9 minutes:
						if (Date.now() > current_time + 9*60000){
							clearInterval(validation_interval)
							location.reload();
						}
						check_for_phone_login_validation(phone_number, validation_interval)
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

//////

$('#email-login-button').click(function(){
	show_email_login_form()
})


$('#phone-number-login-button').click(function(){
	show_phone_login_form()
})


function show_email_login_form(){
	$('#phone-number-password-login-form').hide()
	$('#email-login-form').show()
}

function show_phone_login_form(){
	$('#email-login-form').hide()
	$('#phone-number-password-login-form').show()
}


$('#phone-number-password-login-form').submit(function(e){
	e.preventDefault();
	var auth_header = get_phone_number_login_auth()
	
	if (!isEmpty(auth_header)){
		$.ajax({
			type: "GET",
			headers: auth_header,
			url: `${api_url_prefix}/login/?method=phone_number&type=rp_acc`,
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
				errorToaster(message = `Login failed`);
			}
		})
	}
})


console.clear();

function get_phone_number_login_auth(){
	var phone_number = $('#phone-number').val().trim()
	var password = $('#password').val().trim()

	if (phone_number.length < 6 || password.length < 2){
		errorToaster(message = `${error_title}, phone number or password not specified.`)
		return {};
	}

	return {"Authorization": "Basic " + btoa(`${phone_number}:${password}`)}
}



// function check_for_phone_login_validation(phone_number, validation_interval){
// 	$.ajax({
// 		headers: {"phone_number": phone_number},
// 		url: `${api_url_prefix}/check-sms-register/`,
// 		success: function(response){
// 			if (response.status == 1){
// 				request_done = true;
// 				swal(
// 					title = `${success_title}: ${phone_number}`,
// 					message = response.message,
// 					style = "success")
				
// 				$('.swal-text').html($('.swal-text').text())
// 				clearInterval(validation_interval);
// 				user_register_token = response.data["token"]
// 				hide_loader_spinner();

// 				setTimeout(() => {
// 					login_request()
// 				}, 100);

// 				// setTimeout(() => {
// 				// 	location.href = location.origin;
// 				// }, 3000);
			
// 			}
// 		},
// 		error: function(){
// 			// errorToaster(message = `${unknown_error_text}: Couldn't validate phone number, try again later.`);
// 		}
// 	})
// }


// $('#sms-login-form').submit(function(e){
// 	e.preventDefault()
// 	try {
// 		var phone_number = $('#phone-number').val().trim()
// 		send_sms_login_request(phone_number)
// 	}
// 	catch {
// 		errorToaster(message = `${unknown_error_text}: Couldn't validate phone number, try again later.`);
// 	}
// })


// function login_request(){
// 	if (user_register_token){
// 		$.ajax({
// 			headers: {"token": user_register_token},
// 			type: "GET",
// 			url: `${api_url_prefix}/login-sms/?method=phone_number&type=rp_acc`,
// 			success: function(response){
// 				if (response){
// 					if (response.status == 1){
// 						swal(
// 							title = success_title,
// 							message = response.message,
// 							style = "success"
// 						)

// 						$('.swal-text').html($('.swal-text').text())
// 						setTimeout(() => {
// 							location.href = location.origin;
// 						}, 3000);
// 					}
// 				}
// 			},
// 			error: function(){
// 				swal(
// 					title = error_title,
// 					message = `${unknown_error_text} \n, Try again or contact administartiors`,
// 					style = "error");
// 				setTimeout(() => {
// 					location.href = location.origin;
// 				}, 5000);
// 			}
// 		})
// 	}
// 	else{
// 		swal(
// 			title = error_title,
// 			message = `${unknown_error_text} \n, Try again or contact administartiors`,
// 			style = "error");
// 		setTimeout(() => {
// 			location.href = location.origin;
// 		}, 5000);
// 	}
// }