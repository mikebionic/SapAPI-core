res_translations_forms = ['resTransId','resId','langId','resNameTrans','resDescTrans','resFullDescTrans']
required_res_translations_fields = ['resNameTrans']

$("body").delegate('.addTranslationBtn','click',function(event){
	resourceData = prepareFormData(res_forms,'');
	resTransData = prepareFormData(res_translations_forms,'');
	if (validateInput(required_res_translations_fields)==true){
		if($('.'+res_forms[0]).val()==''){
			if (validateInput(required_res_fields)==true){
				beforeCreated(resourceData,res_forms[0],url_prefix+"/ui/resource/",function(){
					resTransData = prepareFormData(res_translations_forms,'');
					postResTransData(resTransData,url_prefix+'/ui/res_translations/',res_translations_forms,'translationsTable','htmlData');
				});
			}
			else{warningToaster('Product is not in database!');}
		}
		else{
			postResTransData(resTransData,url_prefix+'/ui/res_translations/',res_translations_forms,'translationsTable','htmlData');
		}
	}
});

var postResTransData = function(formData,url,formFields,listName,responseForm){
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
			else if(response.status == 'updated'){
				successToaster(response.responseText);
				$('.'+response[formFields[0]]).html(response.data);
			}
			else{errorToaster(response.responseText);}
			$(".translationModal").modal("hide");
			for (element in formFields){
				$('.'+formFields[element]).val('');
			}
		}
	})
}

