var category_fields = ['categoryName','categoryDesc','categoryIcon']

$("body").delegate('.categoryIcon','click',function(event){
	ownerIconId = $(this).attr('ownerCategory');
	$("body").delegate('.iconsList img','click',function(event){
		selectedIconSrc = $(this).attr('src');
		selectedIconName = $(this).attr('name');
		selectedIconCategory = $(this).attr('icon_category');
		$(".categoryIcon"+ownerIconId+" img").attr('src',selectedIconSrc);
		$(".categoryIcon"+ownerIconId+" img").attr('name',selectedIconName);
		$(".categoryIcon"+ownerIconId+" img").attr('icon_category',selectedIconCategory);
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

	thisIconName = $(".categoryIcon"+ownerId+" img").attr('name');
	thisIconPath = $(".categoryIcon"+ownerId+" img").attr('src');
	if(thisIconName=="add_to_photos"){
		thisIconName='';
		thisIconPath='';
	}
	else{
		categoryData['categoryIcon']=thisIconName;
		categoryData['categoryIconPath']=thisIconPath;
	}
	postFormData(categoryData,url_prefix+"/admin/category/","htmlData","categoriesList"+ownerId);
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
	deleteForm(({"catId":ownerId}),url_prefix+"/admin/category/");
	$(this).parent().parent().remove();
})