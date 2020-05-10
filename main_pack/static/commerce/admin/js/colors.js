
color_forms = ['colorId','colorName','colorDesc','colorCode']
required_color_fields = ['colorName']

$("body").delegate('.addColorBtn','click',function(event){
	colorData = prepareFormData(color_forms,'');
	if (validateInput(required_color_fields)==true){
		postColorData(colorData,'/commerce/ui/color/',color_forms,'colorsList','htmlData');
	}
});

var postColorData = function(formData,url,formFields,listName,responseForm){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'POST',
		url : url,
		success: function(response){
			if(response.status == 'created'){
				$('.'+listName).append(response[responseForm]);
				successToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
			for (element in formFields){
				$('.'+formFields[element]).val('');
			}
		}
	})
}

