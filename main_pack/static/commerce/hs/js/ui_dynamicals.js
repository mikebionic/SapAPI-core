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
	position: 'bottomRight'
	});
}

//////// working with forms ///////

function clearFields(formFields,formId){
	for (element in formFields){
		$('.'+formFields[element]+formId).val('');
	}
}

function clearOwnerFields(formFields,formId){
	for (element in formFields){
		$('.'+formFields[element]+'[ownerId='+formId+']').val('');
		$('.'+formFields[element]+'[ownerId='+formId+']').text('');
	}
}

/////// backend requests //////

function getRegNo(url){
	$.ajax({
		type : 'GET',
		url : url,
		success: function(response){
			// regForm returns a special area to place the data
		$('.'+response.regNoForm).val(response.regNo);
		}
	});
}

function validateInput(requiredFields){
	// universal method for all fields!!
	var fieldsStatus = true
	for (field in requiredFields){
		thisField = $('.'+requiredFields[field]);
		if (thisField.val() == ""){
			if (thisField.attr('placeholder') != null){
				element = thisField.attr('placeholder')
			}
			else {element = thisField.attr('id')}
			errorToaster('Please, fill the data: '+element);
			fieldsStatus = false
		}
	}
	if (fieldsStatus == false){return false;}
	else {return true;}
}

function prepareFormData(formFields,formId){
	var formData = {};
	function buildData(value){
		if ($('.'+value+formId).val() == ""){
			this.value = null;
		}
		else{
			formData[value] = $('.'+value+formId).val();
		}
	}
	formFields.forEach(buildData);
	return formData;
}

function prepareOwnerFormData(formFields,formId=null){
	var formData = {};
	function buildData(value){
		if (formId>0 || formId>''){
			formValue = $('.'+value+'[ownerId='+formId+']').val();
		}
		else{
			formValue = $('.'+value).val();
		}
		if (formValue == ""){
			this.value = null;
		}
		else{
			formData[value] = formValue;
		}
	}
	formFields.forEach(buildData);
	return formData;
}

function validateOwnerInput(requiredFields,formId=null){
	var fieldsStatus = true
	for (field in requiredFields){
		if (formId>0 || formId>''){
			thisField = $('.'+requiredFields[field]+'[ownerId='+formId+']');
		}
		else{
			thisField = $('.'+requiredFields[field]);
		}
		if (thisField.val() == ""){
			if (thisField.attr('placeholder') != null){
				element = thisField.attr('placeholder')
			}
			else {element = thisField.attr('id')}
			errorToaster('Please, fill the data: '+element);
			fieldsStatus = false
		}
	}
	if (fieldsStatus == false){return false;}
	else {return true;}
}


var postData = function(payload_data,url,type,formId,listName,responseForm,alertStyle){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(payload_data),
		type:type,
		url:url,
		success:function(response){
			if (response.status == 'created'){
				$(`.${listName}`).prepend(response[responseForm]);
				if (alertStyle == 'swal'){
					swal(title=success_title,desc=response.responseText,style="success");
				}
				else{
					successToaster(response.responseText);
				}
			}
			else if (response.status == 'updated'){
				if (alertStyle == 'swal'){
					swal(title=success_title,desc=response.responseText,style="success");
				}
				else{
					successToaster(response.responseText);
				}
			}
			else if (response.status == 'deleted'){
				if (alertStyle == 'swal'){
					swal(title=success_title,desc=response.responseText,style="success");
				}
				else{
					successToaster(response.responseText);
				}
				$(`[ownerId=${formId}]`).remove();
			}
			else{
				if (alertStyle == 'swal'){
					swal(title=error_title,desc=response.responseText,style="warning");
				}
				else{
					errorToaster(response.responseText);
				}
			}
		}
	})
}
