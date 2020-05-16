$(document).ready(function(e){
	$('#upload').on('click', function () {
		var form_data = new FormData();
		var ins = document.getElementById('multiFiles').files.length;
		
		if(ins == 0) {
			$('#msg').html('<span style="color:red">Select at least one file</span>');
			return;
		}
		
		for (var x = 0; x < ins; x++) {
			form_data.append("files[]", document.getElementById('multiFiles').files[x]);
		}

		$.ajax({
			url: '/commerce/ui/uploadImages/',
			dataType: 'json',
			cache: false,
			contentType: false,
			processData: false,
			data: form_data,
			type: 'post',
			success: function (response){
				$('.saveImagesBtn').show();
				$('#msg').html('');
				$('.uploadedImagesCard').show("slow");
				for (file in response.files){
					responseImage = response.files[file]["htmlData"];
					$('.imagesList').append(responseImage);
				}
				$.each(response, function (key, data) {							
					if(key !== 'message') {
						$('#msg').append(key + ' -> ' + data + '<br/>');
					} else {
						$('#msg').append(data + '<br/>');
					}
				})
			},
			error: function (response) {
				$('#msg').html(response.message);
			}
		});
	});
});

$("body").delegate('.removeImageBtn','click',function(event){
	$(this).parent().parent().parent().remove();
});

///////////  saving to db  ///////////////

image_forms = ['imgId','empId','companyId','rpAccId','resId','fileName','fileHash','image']

$("body").delegate('.saveImagesBtn','click',function(event){
	resourceData = prepareFormData(res_forms,'');
	imageData = prepareImagesData(image_forms);
	if($('.'+res_forms[0]).val()==''){
		if (validateInput(required_res_fields)==true){
			beforeCreated(resourceData,res_forms[0],"/commerce/ui/resource/",function(){
				postImageData(imageData,'/commerce/ui/images/','POST');
			});
		}
		else{warningToaster('Product is not in database!');}
	}
	else{
		postImageData(imageData,'/commerce/ui/images/','POST');
	}
});

//////// this is the only working for now //////
function imagesDict(formFields){
	var imageData = {};
	function buildData(value){
		if ($('.'+value).val() == ""){
			this.value = null;
		}
		else{
			imageData[value] = $('.'+value).val();
		}
	}
	formFields.forEach(buildData);
	return imageData;
}

function prepareImagesData(){
	var allImages = [];
	$('.imagesList .fileName').each(function(){
		imageData=imagesDict(image_forms);
		imageData['fileName']=$(this).val();
		allImages.push(imageData);
	});
	return allImages;
}
///////////////////////////
var postImageData = function(formData,url,type){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : type,
		url : url,
		success: function(response){
			if(response.status == 'created'){
				successToaster(response.responseText);
				resppp = response
				console.log(response)
				$('.imagesList .fileName').each(function(){
					for(image in response.responses){
						console.log(image)
						fileName = response.responses[image]["fileName"];
						imgId = response.responses[image]["imgId"];
						if($(this).val()==fileName){
							$(this).prev().val(imgId);
						}
					}
				});
				$('.saveImagesBtn').hide();
			}
			else if(response.status == 'deleted'){
				warningToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
		}
	})
}


$("body").delegate('.imagesList .singleImage','click',function(event){
	$('.imagesList .fileName').prev().attr('class','imgId')
	$('.imagesList .fileName:checked').prev().attr('class','imgId mainImageId')
});