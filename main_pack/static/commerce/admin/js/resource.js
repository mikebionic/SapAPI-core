res_forms = ['resId','companyId','divisionId','resCategoryId','unitId',
	'brandId',	'usageStatusId','resTypeId','mainImageId','resMakerId',
	'lastVendorId','resRegNo','resName','resDesc','resFullDesc','resWidth',
	'resHeight','resLength','resWeight','resOnSale','resMinSaleAmount',
	'resMaxSaleAmount','resMinSalePrice','resMaxSalePrice']

required_res_fields = ['resRegNo','resName']

barcode_forms = ['barcodeId','companyId','divisionId','resId','unitId','barcodeVal']
required_barcode_fields = ['barcodeVal']
// places the num into .resRegNo
getRegNo("/commerce/ui/resource/")


function getMainImage(){
	mainImage = $('.imagesList input:checked').attr('name');
	console.log("main image is "+mainImage)
}

/// setting the brand of resource
$("body").delegate('.brandsList .resBrandId','click',function(event){
	$('.brandsList .resBrandId').attr('class','selectgroup-input resBrandId')
	$('.brandsList .resBrandId:checked').attr('class','selectgroup-input resBrandId" brandId')
});


$("body").delegate('.submitButton','click',function(event){
	resourceData = prepareFormData(res_forms,'');
	console.log(resourceData);
	if (validateInput(required_res_fields)==true){
		postResData(resourceData,"/commerce/ui/resource/",res_forms[0]);
	}
	event.preventDefault();
});

$("body").delegate('.addBarcodeBtn','click',function(event){
	resourceData = prepareFormData(res_forms,'');
	barcodeData = prepareFormData(barcode_forms,'');
	if (validateInput(required_barcode_fields)==true){
		if($('.'+res_forms[0]).val()==''){
			if (validateInput(required_res_fields)==true){
				beforeCreated(resourceData,res_forms[0],"/commerce/ui/resource/",function(){
					barcodeData = prepareFormData(barcode_forms,'');
					postBarcodeData(barcodeData,'/commerce/ui/barcode/',barcode_forms[0],'barcodeList','htmlData');
				});
			}
			else{warningToaster('Product is not in database!');}
		}
		else{
			postBarcodeData(barcodeData,'/commerce/ui/barcode/',barcode_forms[0],'barcodeList','htmlData');
		}
	}
});

var postBarcodeData = function(formData,url,responseId,listName,responseForm){
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
			else if(response.status == 'updated'){
				successToaster(response.responseText);
				$('.'+response[responseId]).html(response.data);
			}
			else{errorToaster(response.responseText);}
			$('.barcodeVal').val('');
		}
	})
}



var beforeCreated=function(formData,formId,url,callback){
	$.ajax({
	  contentType: "application/json",
	  dataType: 'json',
	  data : JSON.stringify(formData),
	  type : 'POST',
	  url : url,
	  success: function(response){
		$('.'+formId).val(response[formId]);
		if (response.status == 'regGenerated'){
			warningToaster(response.responseText);
			$('.resRegNo').val(response.regNo)
		}
		if(response.status == 'created'||response.status == 'updated') {
			successToaster(response.responseText);
		}
		callback();
	  }
	})
}

var postResData = function(formData,url,formId){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'POST',
		url : url,
		success: function(response){
			if(response.status == 'created'||response.status == 'updated') {
				successToaster(response.responseText);
				$('.'+formId).val(response[formId]);
			}
			else if(response.status == 'regGenerated'){
				warningToaster(response.responseText);
				$('.resRegNo').val(response.regNo)
			}
			else{errorToaster(response.responseText);}
		}
	})
}
