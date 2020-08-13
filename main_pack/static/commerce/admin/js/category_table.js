var category_forms = ['categoryId','categoryName','categoryDesc','categoryOwner','categoryIcon']
var required_category_fields = ['categoryName']

$("body").delegate('.saveCategoryBtn','click',function(event){
	ownerId = $(this).attr('ownerId');
	console.log("savig category. owner is "+ownerId)
	categoryData = prepareOwnerTableData(category_forms,ownerId);

	thisIconName = $(".categoryIcon"+"[ownerId="+ownerId+"]").attr('name');
	thisIconPath = $(".categoryIcon"+"[ownerId="+ownerId+"]").attr('src');

	categoryData['categoryIcon']=thisIconName;
	categoryData['categoryIconPath']=thisIconPath;

	console.log(categoryData);
	postData(categoryData,url_prefix+"/ui/category_table/",'POST',category_forms[0],'categoryTable','htmlData');
	if (!ownerId || ownerId=='undefined'){
		clearOwnerFields(category_forms,ownerId);
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
		console.log(formId)
		console.log(formValue)
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

$('body').delegate('.deleteCategoryBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	data = {"categoryId":ownerId};
	postData(formData=data,url=url_prefix+"/ui/category_table/",type="DELETE",formId=ownerId);
})

///
$('.newCategoryBtn').click(function(e){
  $('.newCategoryForm').show('slow');
});
$('.saveCategoryBtn').click(function(e){
  $('.newCategoryForm').hide('slow');
});
///

$("body").delegate('.categoryIcon','click',function(event){
	ownerId = $(this).attr('ownerId');
	console.log(ownerId);
	$("body").delegate('.iconsList .singleIcon','click',function(event){
		selectedIconSrc = $(this).attr('src');
		selectedIconName = $(this).attr('name');
		selectedIconCategory = $(this).attr('icon_category');
		console.log(selectedIconCategory)
		$(".categoryIcon"+'[ownerId='+ownerId+"]").attr('src',selectedIconSrc);
		$(".categoryIcon"+'[ownerId='+ownerId+"]").attr('name',selectedIconName);
		$(".categoryIcon"+'[ownerId='+ownerId+"]").attr('icon_category',selectedIconCategory);
		$("#catIconsModal").modal("hide");
	})
})
