///////////// dynamicals ////////////
var successToaster = function(message){
	iziToast.success({
	title: 'Success!',
	message: message,
	position: 'topRight'
  });
}
var errorToaster = function(message){
	iziToast.error({
	title: 'Error!',
	message: message,
	position: 'topRight'
  });
}
var warningToaster = function(message){
	iziToast.warning({
	title: 'Warning!',
	message: message,
	position: 'topCenter'
  });
}

//////// working with forms ///////

function clearFields(formFields,formId){
	for (element in formFields){
		$('.'+formFields[element]+formId).val('');
	}
}