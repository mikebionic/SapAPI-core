res_color_forms = ['rcId','resId','resColorId']

$("body").delegate('.saveResColorBtn','click',function(event){
	resourceData = prepareFormData(res_forms,'');
	resColorData = prepareResColorData();
	console.log(resColorData);
	if($('.'+res_forms[0]).val()==''){
		if (validateInput(required_res_fields)==true){
			beforeCreated(resourceData,res_forms[0],"/commerce/ui/resource/",function(){
				postResColorData(resColorData,'/commerce/ui/res_color/','POST');
			});
		}
		else{warningToaster('Product is not in database!');}
	}
	else{
		postResColorData(resColorData,'/commerce/ui/res_color/','POST');
	}
});

//////// this is the only working for now //////
function resColorsDict(formFields){
	var resColorData = {};
	function buildData(value){
		if ($('.'+value).val() == ""){
			this.value = null;
		}
		else{
			resColorData[value] = $('.'+value).val();
		}
	}
	formFields.forEach(buildData);
	return resColorData;
}

function prepareResColorData(){
	var allData = [];
	$('.colorsList .resColorId:checked').each(function(){
		resColorData=resColorsDict(res_color_forms);
		resColorData['resColorId']=$(this).val();
		allData.push(resColorData);
	});
	return allData;
}
///////////////////////////
var postResColorData = function(formData,url,type){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : type,
		url : url,
		success: function(response){
			if(response.status == 'created'){
				successToaster(response.responseText);
				// $('.saveResColorBtn').hide();
			}
			else if(response.status == 'deleted'){
				warningToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
		}
	})
}
