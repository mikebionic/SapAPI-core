slider_forms = ['sliderId','companyId','divisionId','sliderName','sliderDesc']
required_slider_fields = ['sliderName']
sider_image_forms = ['sliderImgId','sliderId','sliderImgName','sliderImgDesc',
	'sliderImgMainImgFileName','sliderImgSubImageFileName1','sliderImgSubImageFileName2',
	'sliderImgSubImageFileName3','sliderImgSubImageFileName4','sliderImgSubImageFileName5',
	'sliderImgStartDate','sliderImgEndDate']

$("body").delegate('.saveSliderBtn','click',function(event){
	ownerId = $(this).attr('ownerId');
	console.log("savig slider. owner is "+ownerId)
	sliderData = prepareOwnerFormData(slider_forms,ownerId);
	console.log(sliderData);
	if (validateOwnerInput(required_slider_fields,ownerId)==true){
		postData(sliderData,url_prefix+"/ui/slider/",'POST',slider_forms[0],'slidersList','htmlData');
	}
	event.preventDefault();
});

function clearNewSliderFields(){
	$('.newSliderCard').hide('slow');
	$('.newSliderCard input').val('');
	$('.newSliderCard textarea').val('');
}

var postData = function(formData,url,type,formId,listName,responseForm){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type:type,
		url:url,
		success:function(response){
			if (response.status == 'created'){
				$('.'+listName).prepend(response[responseForm]);
				successToaster(response.responseText);
				clearNewSliderFields()
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
	$('.sliderName'+'[ownerId='+ownerId+']').replaceWith("<input class='form-control sliderName' ownerId="+ownerId+" value="+"'"+currentName+"'"+" >");
	$('.sliderDesc'+'[ownerId='+ownerId+']').replaceWith("<input class='form-control sliderDesc' ownerId="+ownerId+" value="+"'"+currentDesc+"'"+" >");
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