size_type_forms = ['sizeTypeId','sizeTypeName','sizeTypeDesc']
res_size_forms = ['rsId','resId','sizeId']

$("body").delegate('.saveResSizeBtn','click',function(event){
	resourceData = prepareFormData(res_forms,'');
	resSizeData = prepareResSizeData();
	console.log(resSizeData)
	if($('.'+res_forms[0]).val()==''){
		if (validateInput(required_res_fields)==true){
			beforeCreated(resourceData,res_forms[0],"/commerce/ui/resource/",function(){
				postResSizeData(resSizeData,'/commerce/ui/res_size/','POST');
			});
		}
		else{warningToaster('Product is not in database!');}
	}
	else{
		postResSizeData(resSizeData,'/commerce/ui/res_size/','POST');
	}
});

//////// this is the only working for now //////
function resSizeDict(formFields){
	var resSizeData = {};
	function buildData(value){
		if ($('.'+value).val() == ""){
			this.value = null;
		}
		else{
			resSizeData[value] = $('.'+value).val();
		}
	}
	formFields.forEach(buildData);
	return resSizeData;
}

function prepareResSizeData(){
	var allData = [];
	$('.sizesList .rsId:checked').each(function(){
		resSizeData=resSizeDict(res_size_forms);
		resSizeData['rsId']=$(this).val();
		allData.push(resSizeData);
	});
	return allData;
}
///////////////////////////
var postResSizeData = function(formData,url,type){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : type,
		url : url,
		success: function(response){
			if(response.status == 'created'){
				successToaster(response.responseText);
				// $('.saveResSizeBtn').hide();
			}
			else if(response.status == 'deleted'){
				warningToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
		}
	})
}
