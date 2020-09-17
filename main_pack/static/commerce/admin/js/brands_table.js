$('body').delegate('.deleteBrandBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	data = {"brandId":ownerId};
	postData(formData=data,url=url_prefix+"/ui/brands_table/",type="DELETE",alertStyle="swal",formId=ownerId);
})