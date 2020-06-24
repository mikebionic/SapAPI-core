slider_forms = ['sliderId','companyId','divisionId','sliderName','sliderDesc']
required_slider_fields = ['sliderName']
sider_image_forms = ['sliderImgId','sliderId','sliderImgName','sliderImgDesc',
	'sliderImgMainImgFileName','sliderImgSubImageFileName1','sliderImgSubImageFileName2',
	'sliderImgSubImageFileName3','sliderImgSubImageFileName4','sliderImgSubImageFileName5',
	'sliderImgStartDate','sliderImgEndDate']

$("body").delegate('.saveSliderBtn','click',function(event){
	sliderData = prepareFormData(slider_forms,'');
	console.log(sliderData);
	if (validateInput(required_slider_fields)==true){
		postData(sliderData,url_prefix+"/ui/slider/",'POST',slider_forms[0],'slidersList','htmlData');
	}
	event.preventDefault();
});

var postData = function(formData,url,type,formId,listName,responseForm){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type:type,
		url:url,
		success:function(response){
			if (response.status == 'created') {
				$('.'+listName).prepend(response[responseForm]);
				successToaster(response.responseText);
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

$('body').delegate('.addSliderImageBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	$('.addSliderImageModal').show();
})

$('body').delegate('.editSliderBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	editSlidersUi(ownerId)
})

$('body').delegate('.deleteSliderBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	data = {"sliderId":ownerId};
	postData(formData=data,url=url_prefix+"/ui/slider/",type="delete",formId=ownerId);
})

function editSlidersUi(ownerId){
	$('.editSliderBtn'+'[ownerId='+ownerId+']').hide('slow');
	$('.saveSliderBtn'+'[ownerId='+ownerId+']').show('slow');
	$('.cancelEditSliderBtn'+'[ownerId='+ownerId+']').show('slow');
	$('.deleteSliderBtn'+'[ownerId='+ownerId+']').show('slow');
	var currentName = $('.sliderName'+'[ownerId='+ownerId+']').text();
	var currentDesc = $('.sliderDesc'+'[ownerId='+ownerId+']').text();
	$('div .sliderName'+'[ownerId='+ownerId+']').html("<input class='form-control sliderName' ownderId="+ownerId+" value="+"'"+currentName+"'"+" >");
	$('div .sliderDesc'+'[ownerId='+ownerId+']').html("<input class='form-control sliderDesc' ownderId="+ownerId+" value="+"'"+currentDesc+"'"+" >");
	
	$('body').delegate('.cancelEditSliderBtn','click',function(){
		ownerId = $(this).attr('ownerId');
		cancelEditSlidersUi(ownerId,currentName,currentDesc)
	})
}
function cancelEditSlidersUi(ownerId,oldName,oldDesc){
	$('.editSliderBtn'+'[ownerId='+ownerId+']').show('slow');
	$('.saveSliderBtn'+'[ownerId='+ownerId+']').hide('slow');
	$('.cancelEditSliderBtn'+'[ownerId='+ownerId+']').hide('slow');
	$('.deleteSliderBtn'+'[ownerId='+ownerId+']').hide('slow');
	$('.sliderName'+'[ownerId='+ownerId+']').html("<div class='sliderName' ownderId="+ownerId+">"+oldName+"</div>");
	$('.sliderDesc'+'[ownerId='+ownerId+']').html("<div class='sliderDesc' ownderId="+ownerId+">"+oldDesc+"</div>");
}

// other UI actions
$('.newSliderBtn').click(function(e){
  $('.newSliderCard').show('slow');
});
$('.addSliderBtn').click(function(e){
  $('.newSliderCard').hide('slow');
});
///////


$('body').delegate('#upload','click',function(){
	ownerId = $(this).attr('ownerId');
	uploadImage(ownerId)
})
function uploadImage(ownerId){
	var form_data = new FormData();
	var ins = document.getElementById('multiFiles').files.length;
	if(ins == 0) {
		$('#msg').html('<span style="color:red">Select at least one file</span>');
		return;
	}
	for (var x = 0; x < ins; x++) {
		form_data.append("files[]", document.getElementById('multiFiles').files[x]);
	}
	form_data.append("sliderId",ownerId)
	console.log(form_data)

	$.ajax({
		url: url_prefix+'/ui/uploadSliderImages/',
		dataType: 'json',
		cache: false,
		contentType: false,
		processData: false,
		data: form_data,
		type: 'post',
		success: function (response){
			for (file in response.files){
				responseImage = response.files[file]["htmlData"];
				$('.sliderImagesList').append(responseImage);
			}
		}
	});
}

///////////  saving to db  ///////////////

// image_forms = ['imgId','empId','companyId','rpAccId','resId','fileName','fileHash','image']

// $("body").delegate('.saveImagesBtn','click',function(event){
// 	resourceData = prepareFormData(res_forms,'');
// 	imageData = prepareImagesData(image_forms);
// 	if($('.'+res_forms[0]).val()==''){
// 		if (validateInput(required_res_fields)==true){
// 			beforeCreated(resourceData,res_forms[0],url_prefix+"/ui/resource/",function(){
// 				postImageData(imageData,url_prefix+'/ui/images/','POST');
// 			});
// 		}
// 		else{warningToaster('Product is not in database!');}
// 	}
// 	else{
// 		postImageData(imageData,url_prefix+'/ui/images/','POST');
// 	}
// });

// //////// this is the only working for now //////
// function imagesDict(formFields){
// 	var imageData = {};
// 	function buildData(value){
// 		if ($('.'+value).val() == ""){
// 			this.value = null;
// 		}
// 		else{
// 			imageData[value] = $('.'+value).val();
// 		}
// 	}
// 	formFields.forEach(buildData);
// 	return imageData;
// }

// function prepareImagesData(){
// 	var allImages = [];
// 	$('.imagesList .fileName').each(function(){
// 		imageData=imagesDict(image_forms);
// 		imageData['fileName']=$(this).val();
// 		allImages.push(imageData);
// 	});
// 	return allImages;
// }
// ///////////////////////////
// var postImageData = function(formData,url,type){
// 	$.ajax({
// 		contentType:"application/json",
// 		dataType:"json",
// 		data:JSON.stringify(formData),
// 		type : type,
// 		url : url,
// 		success: function(response){
// 			if(response.status == 'created'){
// 				successToaster(response.responseText);
// 				resppp = response
// 				console.log(response)
// 				$('.imagesList .fileName').each(function(){
// 					for(image in response.responses){
// 						console.log(image)
// 						fileName = response.responses[image]["fileName"];
// 						imgId = response.responses[image]["imgId"];
// 						if($(this).val()==fileName){
// 							$(this).prev().val(imgId);
// 						}
// 					}
// 				});
// 				$('.saveImagesBtn').hide();
// 			}
// 			else if(response.status == 'deleted'){
// 				warningToaster(response.responseText);
// 			}
// 			else{errorToaster(response.responseText);}
// 		}
// 	})
// }


// $("body").delegate('.imagesList .singleImage','click',function(event){
// 	$('.imagesList .fileName').prev().attr('class','imgId')
// 	$('.imagesList .fileName:checked').prev().attr('class','imgId mainImageId')
// });