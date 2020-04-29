
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
		console.log("desc owner: "+ownerModalId);
		$(".descContent").val('');
	$("body").delegate('.submitDescBtn','click',function(event){
		description = $(".descContent").val();
		console.log("heres desc: "+description);
		$(".categoryDesc"+ownerModalId).val(description);
		$(".categoryDescModal").modal("hide");
	})
})

$("body").delegate('.addCategoryBtn','click',function(event){
	ownerId = $(this).attr('ownerCategory');
	console.log(ownerId);
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

	console.log(categoryData);
	postFormData(categoryData,"/commerce/admin/category/","htmlData","categoriesList"+ownerId);
	clearFields(category_fields,ownerId);
})

function clearFields(formFields,formId){
	for (element in formFields){
		$('.'+formFields[element]+formId).val('');
	}
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
				console.log("Response form is : "+response[responseForm]);
				successToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
		}
	})
}

//////////// using the html tag appends not render template style ////
// listName is an appending field like <ul> or <div>
// formFields are the fields containing needed data
// formData is the json ready-to-send data
// responseId will be used for updates
// responseId is the required json data we want to get, as "catId"

// var postFormData = function(formData,url,responseId,listName,formFields){
// 	$.ajax({
// 		contentType:"application/json",
// 		dataType:"json",
// 		data:JSON.stringify(formData),
// 		type : 'POST',
// 		url : url,
// 		success: function(response){
// 			// if (response.status == 'updated'){
// 			// 	successToaster(response.responseText);
// 			// 	$('#'+response[responseId]).html(response.data);
// 			// }
// 			if (response.status == 'created') {
// 				$('.'+listName).prepend('<tr id="'+response[responseId]+'">'+response.data+'</tr>');
// 				successToaster(response.responseText);
// 			}
// 			else{errorToaster(response.responseText);}
// 			for (element in formFields){
// 				$('#'+formFields[element]).val('');
// 			}
// 		}
// 	})
// }
//////////////////////////

// var url = {{url_for(admin.dashboard_commerce)}}

// function postEmpData(employeeData){
// 	$.ajax({
// 	  contentType: "application/json",
// 	  dataType: 'json',
// 	  data : JSON.stringify(employeeData),
// 	  type : 'POST',
// 	  url : '/ui/employee/', 
// 	  success: function(response){
// 		if (response.status == 'regGenerated'){
// 			warningToaster(response.responseText);
// 		}
// 		if (response.status == 'updated'){
// 			successToaster(response.responseText);
// 			$('#'+response.empId).html(response.data);
// 			removeTab('.updateEmpTabBtn','.updateEmpTab');
// 			removeTab('.addEmpTabBtn','.addEmpTab');
// 		}
// 		else{
// 			$('#employeesTable').prepend('<tr id="'+response.empId+'">'+response.data+'</tr>');
// 			removeTab('.addEmpTabBtn','.addEmpTab');
// 			successToaster(response.responseText);
// 		}
// 	  }
// 	});
// }