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
		postData(sliderData,url_prefix+"/ui/slider/",slider_forms[0],'slidersList','htmlData');
	}
	event.preventDefault();
});

var postData = function(formData,url,formId,listName,responseForm){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type:'POST',
		url:url,
		success:function(response){
			if (response.status == 'created') {
				$('.'+listName).prepend(response[responseForm]);
				successToaster(response.responseText);
			}
			else if (response.status == 'updated'){
				successToaster(response.responseText);
			}
			else{errorToaster(response.responseText);}
		}
	})
}

$('body').delegate('.addSliderImageBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	$('.uploadSliderCard'+'[ownerId='+ownerId+']').show('slow');
})



$('body').delegate('.editSliderBtn','click',function(){
	ownerId = $(this).attr('ownerId');
	$('.newSliderCard'+'[ownerId='+ownerId+']').show('slow');
	editSlidersUi(ownerId)
})

function editSlidersUi(ownerId){
	var currentName = $('.sliderName'+'[ownerId='+ownerId+']').text()
	var currentDesc = $('.sliderDesc'+'[ownerId='+ownerId+']').text()
	$('div .sliderName'+'[ownerId='+ownerId+']').html("<input class='form-control sliderName' ownderId="+ownerId+" value="+"'"+currentName+"'"+" >")
	$('div .sliderDesc'+'[ownerId='+ownerId+']').html("<input class='form-control sliderDesc' ownderId="+ownerId+" value="+"'"+currentDesc+"'"+" >")
}
// $('body').delegate('.addToCart','click',function(){
// 	$(this).hide();
// 	ownerId = $(this).attr('ownerId');
// 	addToCart(ownerId);
// })

// function addToCart(ownerId){
// 	$('.removeFromCart'+'[ownerId='+ownerId+']').show();
// 	priceValue=$('.priceValue'+'[ownerId='+ownerId+']').attr('value');
// 	productQty=$('.productQty'+'[ownerId='+ownerId+']').val();
// 	if(productQty>1){}else{
// 		productQty=1;
// 	}
// 	// saving cookie
// 	productData={'resId':ownerId,'priceValue':priceValue,'productQty':productQty};
// 	cartData['product'+ownerId]=productData;
// 	Cookies.set('cart',JSON.stringify(cartData));
// 	// sending request
// 	cartOperations(productData,url_prefix+'/product/ui_cart/','POST','htmlData','cartItemsList');
// 	qtyCheckout(ownerId,productQty);
// 	totalPriceCheckout(ownerId)
// }

// other UI actions
$('.newSliderBtn').click(function(e){
  $('.newSliderCard').show('slow');
});
$('.addSliderBtn').click(function(e){
  $('.newSliderCard').hide('slow');
});

