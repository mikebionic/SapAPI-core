var rating_forms = ['ratingId','ratingValue','ratingRemark','ratingValidated']

$("body").delegate('.saveRatingBtn','click',function(event){
	ownerId = $(this).attr('ownerId');
	categoryData = prepareOwnerTableData(rating_forms,ownerId);

	ratingValidated = $(".ratingValidated"+"[ownerId="+ownerId+"]").prop('checked');
	categoryData['ratingValidated'] = ratingValidated;

	postData(categoryData,url_prefix+"/ui/rating_table/",'POST',rating_forms[0],'categoryTable','htmlData');
	if (!ownerId || ownerId == 'undefined'){
		clearOwnerFields(rating_forms,ownerId);
	}
	event.preventDefault();
});

function prepareOwnerTableData(formFields,formId=null){
	var formData = {};
	function buildData(value){
		if (formId>0 || formId>''){
			formValue = $('.'+value+'[ownerId='+formId+']').text();
		}
		else{
			formValue = $('.'+value).text();
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

$('body').delegate('.deleteRatingBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	data = {"categoryId":ownerId};
	postData(formData=data,url=url_prefix+"/ui/rating_table/",type="DELETE",formId=ownerId);
})
