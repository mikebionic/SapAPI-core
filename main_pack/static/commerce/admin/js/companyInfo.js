companyInfo_fields = ['companyName','companyFullName','companyDesc','companyAccInfId',
		'companyAddress','companyAddressLegal','companyLatitude','companyLongitude',
		'companyPhone1','companyPhone2','companyPhone3','companyPhone4',
		'companyPostalCode','companyEmail','companyWTime']

$("body").delegate('.submitCompanyInfo','click',function(event){
	companyData = prepareCompanyInfo(companyInfo_fields,'');
	postCompanyInfo(companyData,"/commerce/admin/company/");
})

function prepareCompanyInfo(formFields,formId){
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

var postCompanyInfo = function(formData,url){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'POST',
		url : url,
		success: function(response){
			if (response.status == 'updated'){
				successToaster(response.responseText);
				$(".contactModal").modal("hide");
			}
			else{errorToaster(response.responseText);}
		}
	})
}