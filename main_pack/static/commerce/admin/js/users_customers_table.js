// dom click events
$("body").delegate('.setRpAccType','click',function(){
	ownerId = $(this).attr('ownerId');
	setRpAccType(ownerId);
});

$("body").delegate('.setRpAccStatus','click',function(){
	ownerId = $(this).attr('ownerId');
	setRpAccStatus(ownerId);
});

$('body').delegate('.deleteCustomerBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	data = {"rpAccId":ownerId};
	postData(formData=data,url=url_prefix+"/ui/customers_table/",type="DELETE",formId=ownerId);
})

$("body").delegate('.setUserType','click',function(){
	ownerId = $(this).attr('ownerId');
	setUserType(ownerId);
});

$('body').delegate('.deleteUserBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	data = {"userId":ownerId};
	postData(formData=data,url=url_prefix+"/ui/users_table/",type="DELETE",formId=ownerId);
})

// ajax functions
function setRpAccStatus(ownerId){
	data = {
		'rpAccId':ownerId,
		'rpAccStatusId':$('.rpAccStatus:selected'+'[ownerId='+ownerId+']').val()
	}
	postData(formData=data,url=url_prefix+'/ui/customers_table/',type='POST');
}

function setRpAccType(ownerId){
	data = {
		'rpAccId':ownerId,
		'rpAccTypeId':$('.rpAccType:selected'+'[ownerId='+ownerId+']').val()
	}
	postData(formData=data,url=url_prefix+'/ui/customers_table/',type='POST');
}

function setUserType(ownerId){
	data = {
		'userId':ownerId,
		'userTypeId':$('.userType:selected'+'[ownerId='+ownerId+']').val()
	}
	postData(formData=data,url=url_prefix+'/ui/users_table/',type='POST');
}