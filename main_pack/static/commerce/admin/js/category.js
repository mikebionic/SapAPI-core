var category_fields = ['categoryId','categoryName','categoryDesc','categoryIcon']

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

$("body").delegate('.editCategoryBtn','click',function(event){
	ownerId = $(this).attr('ownerId');
	categoryName=$('.categoryName'+'[ownerId='+ownerId+']').text();
	categoryDesc=$('.categoryDesc'+'[ownerId='+ownerId+']').attr('value');

	categoryIconName = $('.categoryIcon img'+'[ownerId='+ownerId+']').attr('name');
	categoryIconPath = $('.categoryIcon img'+'[ownerId='+ownerId+']').attr('src');
	$('.editCategoryName').val(categoryName);
	$('.editCategoryDesc').val(categoryDesc);
	$(".editCategoryIcon img").attr('name',categoryIconName);
	$(".editCategoryIcon img").attr('src',categoryIconPath);
	
	$('.editCategoryId').val(ownerId);
	edit_category_fields = ['editCategoryId','editCategoryName','editCategoryDesc','editCategoryIcon']

	$("body").delegate('.saveCategoryBtn','click',function(event){
		categoryName=$('.editCategoryName').val();
		categoryDesc=$('.editCategoryDesc').val();

		$('.categoryName'+'[ownerId='+ownerId+']').text(categoryName);
		$('.categoryDesc'+'[ownerId='+ownerId+']').attr('value',categoryDesc);

		categoryData = prepareFormData(edit_category_fields,'');

		thisIconName = $(".editCategoryIcon img").attr('name');
		thisIconPath = $(".editCategoryIcon img").attr('src');

		categoryData['categoryIcon']=thisIconName;
		categoryData['categoryIconPath']=thisIconPath;
		console.log(categoryData);
		postData(categoryData,url_prefix+"/admin/category/",'POST',ownerId);
		clearFields(edit_category_fields);
	})


	$("body").delegate('.editCategoryIcon','click',function(event){
		ownerIconId = $(this).attr('ownerId');
		$("body").delegate('.iconsList img','click',function(event){
			selectedIconSrc = $(this).attr('src');
			selectedIconName = $(this).attr('name');
			selectedIconCategory = $(this).attr('icon_category');
			$(".editCategoryIcon"+ownerIconId+" img").attr('src',selectedIconSrc);
			$(".editCategoryIcon"+ownerIconId+" img").attr('name',selectedIconName);
			$(".editCategoryIcon"+ownerIconId+" img").attr('icon_category',selectedIconCategory);
			$("#catIconsModal").modal("hide");
		})
	})
})

var postData = function(formData,url,type,formId,listName,responseForm){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type:type,
		url:url,
		success:function(response){
			if (response.status == 'created'){
				$('.'+listName).prepend(response[responseForm]);
				successToaster(response.responseText);
				clearNewSliderFields()
			}
			else if (response.status == 'updated'){
				successToaster(response.responseText);
			}
			else if (response.status == 'deleted'){
				successToaster(response.responseText);
				$('.sliderCard'+'[ownerId='+ownerId+']').remove();
			}
			else{errorToaster(response.responseText);}
		}
	})
}



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
	deleteForm(({"categoryId":ownerId}),url_prefix+"/admin/category/");
	$(this).parent().parent().remove();
})