var category_fields = ['categoryName','categoryDesc','categoryIcon']

$("body").delegate('.categoryIcon','click',function(event){
	ownerIconId = $(this).attr('ownerCategory');
	$("body").delegate('.iconsList i','click',function(event){
		selectedIcon = $(this).attr('class');
		$(".categoryIcon"+ownerIconId+" i").attr('class',selectedIcon);
		$("#catIconsModal").modal("hide");
	})
})

$("body").delegate('.addDescBtn','click',function(event){
	ownerModalId = $(this).attr('ownerCategory');
		$(".descContent").val('');
	$("body").delegate('.submitDescBtn','click',function(event){
		description = $(".descContent").val();
		$(".categoryDesc"+ownerModalId).val(description);
		$(".categoryDescModal").modal("hide");
	})
})

$("body").delegate('.addCategoryBtn','click',function(event){
	ownerId = $(this).attr('ownerCategory');
	if(ownerId==null){ownerId='';}
	categoryData = prepareFormData(category_fields,ownerId);
	categoryData['ownerCategory']=ownerId;

	thisIconName = $(".categoryIcon"+ownerId+" i").attr('class');
	if(thisIconName=="fas fa-apple-alt"){
		thisIconName='';
	}
	else{
		categoryData['categoryIcon']=thisIconName;
	}
	postFormData(categoryData,"/commerce/admin/category/","htmlData","categoriesList"+ownerId);
	clearFields(category_fields,ownerId);
})


var postFormData = function(formData,url,responseForm,listName){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'POST',
		url : url,
		success: function(response){
			if (response.status == 'created') {
				$('.'+listName).prepend(response[responseForm]);
				successToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
		}
	})
}

var deleteForm = function(formData,url){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'DELETE',
		url : url,
		success: function(response){
			if (response.status == 'deleted') {
				warningToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
		}
	})
}

$("body").delegate('.removeCategoryBtn','click',function(event){
	ownerId = $(this).attr('ownerCategory');
	deleteForm(({"catId":ownerId}),"/commerce/admin/category/");
	$(this).parent().parent().remove();
})