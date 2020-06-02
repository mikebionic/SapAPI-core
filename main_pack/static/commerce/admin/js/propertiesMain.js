
function propertyDescShow(fieldName,fieldDesc){
	$("body").delegate('.'+fieldName,'keyup',function(e){
		if(($('.'+fieldName)).val()!=''){
			$('.'+fieldDesc).show('slow');
		}
		else{$('.'+fieldDesc).hide('slow');}
	});
}

//////// size actions ////////////
size_forms = ['sizeId','sizeName','sizeDesc','sizeTypeId']
required_size_fields = ['sizeName']
propertyDescShow('sizeName','sizeDesc');

$("body").delegate('.addSizeBtn','click',function(event){
	sizeData = prepareFormData(size_forms,'');
	if (validateInput(required_size_fields)==true){
		postPropData(sizeData,url_prefix+'/ui/size/',size_forms,'sizesList','htmlData');
	}
});

/////// brand actions /////
brand_forms = ['brandId','brandName','brandDesc']
required_brand_forms = ['brandName']
propertyDescShow('brandName','brandDesc');

$("body").delegate('.addBrandBtn','click',function(event){
	brandData = prepareFormData(brand_forms,'');
	if (validateInput(required_brand_forms)==true){
		postPropData(brandData,url_prefix+'/ui/brand/',brand_forms,'brandsList','htmlData');
	}
});

//////// color actions ////////
color_forms = ['colorId','colorName','colorDesc','colorCode']
required_color_fields = ['colorName']
propertyDescShow('colorName','colorDesc');

$("body").delegate('.addColorBtn','click',function(event){
	colorData = prepareFormData(color_forms,'');
	if (validateInput(required_color_fields)==true){
		postPropData(colorData,url_prefix+'/ui/color/',color_forms,'colorsList','htmlData');
	}
});
///////////////

var postPropData = function(formData,url,formFields,listName,responseForm){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'POST',
		url : url,
		success: function(response){
			if(response.status == 'created'){
				$('.'+listName).append(response[responseForm]);
				successToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
			for (element in formFields){
				$('.'+formFields[element]).val('');
			}
		}
	})
}