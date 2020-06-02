res_price_forms = ['resPriceId','resPriceTypeId','resPriceGroupId','unitId','currencyId',
	'resId','resPriceRegNo','resPriceValue','priceStartDate','priceEndDate']

required_res_price_fields = ['resPriceValue']


getRegNo(url_prefix+"/ui/price/")

$("body").delegate('.savePriceBtn','click',function(event){
	resourceData = prepareFormData(res_forms,'');
	resPriceData = prepareFormData(res_price_forms,'');
	if (validateInput(required_res_price_fields)==true){
		if($('.'+res_forms[0]).val()==''){
			if (validateInput(required_res_fields)==true){
				beforeCreated(resourceData,res_forms[0],url_prefix+"/ui/resource/",function(){
					resPriceData = prepareFormData(res_price_forms,'');
					postPriceData(resPriceData,url_prefix+'/ui/price/',res_price_forms[0]);
				});
			}
			else{warningToaster('Product is not in database!');}
		}
		else{
			postPriceData(resPriceData,url_prefix+'/ui/price/',res_price_forms[0]);
		}
	}
});

var postPriceData = function(formData,url,formId){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'POST',
		url : url,
		success: function(response){
			if(response.status == 'created'||response.status == 'updated'){
				successToaster(response.responseText);
				console.log('responseform '+response[formId])
				$('.'+formId).val(response[formId]);
			}
			else if(response.status == 'regGenerated'){
				warningToaster(response.responseText);
				$('.'+response.regNoForm).val(response.regNo);
			}
			else{errorToaster(response.responseText);}
		}
	})
}