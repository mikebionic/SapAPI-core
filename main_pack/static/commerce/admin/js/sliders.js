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
		clearNewSliderFields();
	}
	event.preventDefault();
});

$("body").delegate('.minimizeSlider','click',function(){
	clearNewSliderFields();
});

function clearNewSliderFields(){
  $('.newSliderBtn').show('slow');
	$('.newSliderCard').hide('slow');
	$('.minimizeSlider').hide('slow');
	$('.newSliderCard input').val('');
	$('.newSliderCard textarea').val('');
};

$('body').delegate('.addSliderImageBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	$('.addSliderImageModal').show();
});

$('body').delegate('.editSliderBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	editSlidersUi(ownerId)
});

$('body').delegate('.deleteSliderBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	data = {"sliderId":ownerId};
	postData(formData=data,url=url_prefix+"/ui/slider/",type="delete",formId=ownerId);
});

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
  $('.newSliderBtn').hide('slow');
  $('.minimizeSlider').show('slow');
});
$('.addSliderBtn').click(function(e){
  $('.newSliderCard').hide('slow');
  $('.minimizeSlider').hide('slow');
  $('.newSliderBtn').show('slow');
});
//////