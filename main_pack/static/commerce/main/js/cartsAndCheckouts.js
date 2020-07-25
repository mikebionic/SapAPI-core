resource_forms = ['resId','resName','resDesc','resPrice','resColor','resSize']

/// getting the cookie data
$(document).ready(function(){
	cartCookie = Cookies.get('cart');
	if(cartCookie==undefined){
		cartData={};
	}
	else{
		cartData=JSON.parse(cartCookie);
		for (i in cartData){
			ownerId = cartData[i]["resId"];
			$('.addToCart'+'[ownerId='+ownerId+']').hide();
			$('.removeFromCart'+'[ownerId='+ownerId+']').show();
			$('.productQty'+'[ownerId='+ownerId+']').val(cartData[i]["productQty"]);
			$('.cartItemQty'+'[ownerId='+ownerId+']').val(cartData[i]["productQty"]);
			$('.uiQtyText'+'[ownerId='+ownerId+']').text(cartData[i]["productQty"]);
		}
		for (i in cartData){
			if (i){
				var do_request = true;
			}
		}
		if (do_request==true){
			cartOperations(cartData,url_prefix+'/product/ui_cart/','PUT','htmlData','cartItemsList');
		}
	}
});


$('body').delegate('.addToWishlist','click',function(){
	$(this).hide();
	ownerId = $(this).attr('ownerId');
	addToWishlist(ownerId);
})

$('body').delegate('.removeFromWishlist','click',function(){
	ownerId = $(this).attr('ownerId');
	removeFromWishlist(ownerId);
});

$('body').delegate('.addToCart','click',function(){
	$(this).hide();
	ownerId = $(this).attr('ownerId');
	addToCart(ownerId);
})

$('body').delegate('.removeFromCart','click',function(){
	ownerId = $(this).attr('ownerId');
	removeFromCart(ownerId);
});

$('body').delegate('.checkoutCartBtn','click',function(){
	cartCookie = Cookies.get('cart');
	data={}
	cartData=JSON.parse(cartCookie);
	data['cartData']=cartData;
	data['orderDesc']=$('.orderDesc').val();
	checkoutCart(data,url_prefix+'/product/ui_cart_checkout/','POST');
});


function addToWishlist(ownerId){
	productData={'resId':ownerId};
	postData(formData=productData,url=url_prefix+"/product/ui_wishlist/",type="POST",listName='wishlistItems');
	$('.addToWishlist'+'[ownerId='+ownerId+']').hide();
	$('.removeFromWishlist'+'[ownerId='+ownerId+']').show();
}

function removeFromWishlist(ownerId){
	productData={'resId':ownerId};
	postData(formData=productData,url=url_prefix+"/product/ui_wishlist/",type="DELETE",formId=ownerId);
	$('.wishlistObject'+ownerId).remove();
	$('.removeFromWishlist'+'[ownerId='+ownerId+']').hide();
	$('.addToWishlist'+'[ownerId='+ownerId+']').show();
}

function addToCart(ownerId){
	$('.removeFromCart'+'[ownerId='+ownerId+']').show();
	priceValue=$('.priceValue'+'[ownerId='+ownerId+']').attr('value');
	productQty=$('.productQty'+'[ownerId='+ownerId+']').val();
	if(productQty>1){}else{
		productQty=1;
	}
	// saving cookie
	productData={'resId':ownerId,'priceValue':priceValue,'productQty':productQty};
	cartData['product'+ownerId]=productData;
	Cookies.set('cart',JSON.stringify(cartData));
	// sending request
	cartOperations(productData,url_prefix+'/product/ui_cart/','POST','htmlData','cartItemsList');
	qtyCheckout(ownerId,productQty);
	totalPriceCheckout(ownerId)
}

function removeFromCart(ownerId){
	if(ownerId>0){
		$('.cartObject'+ownerId).remove();
		$('.cartTableObject'+ownerId).remove();
		$('.removeFromCart'+'[ownerId='+ownerId+']').hide();
		$('.addToCart'+'[ownerId='+ownerId+']').show();
		delete cartData['product'+ownerId];
		Cookies.set('cart',JSON.stringify(cartData));
		countCartItems();
	}
	else{
		cartData={}
		Cookies.set('cart',JSON.stringify(cartData));
		countCartItems();
	}
}

$('body').delegate('.clearCartBtn','click',function(){
	clearCart();
});

function clearCart(){
	cartCookie = Cookies.get('cart');
	if(cartCookie==undefined){
		cartData={};
	}
	else{
		cartData=JSON.parse(cartCookie);
		for (i in cartData){
			ownerId = cartData[i]["resId"];
			$('.addToCart'+'[ownerId='+ownerId+']').show();
			$('.removeFromCart'+'[ownerId='+ownerId+']').hide();
			$('.cartObject'+ownerId).remove();
			$('.cartTableObject'+ownerId).remove();
			delete cartData['product'+ownerId];
			Cookies.set('cart',JSON.stringify(cartData));
			countCartItems();
		}
	}
}

function countCartItems(){
	var num=0;
	var totalPrice=0;
	$('.cartItemsList li').each(function(){
		num+=1;
	});
	for(i in cartData){
		quantity = cartData[i]['productQty'];
		price = cartData[i]['priceValue'];
		totalPrice+=price*quantity;
	}
	$('.cartItemsFullQty').text(num);
	$('.cartTotalPrice').text(parseFloat(totalPrice).toFixed(2));
}

function qtyCheckout(ownerId,newQtyValue){
	if(newQtyValue<=0){
		newQtyValue=1;
	}
	$('.productQty'+'[ownerId='+ownerId+']').attr('value',newQtyValue);
	$('.cartItemQty'+'[ownerId='+ownerId+']').val(newQtyValue);
	// $('.productQty'+'[ownerId='+ownerId+']').attr('value',newQtyValue);
	$('.uiQtyText'+'[ownerId='+ownerId+']').text(newQtyValue);
	if(cartData['product'+ownerId]!=undefined){
		productData = cartData['product'+ownerId];
		productData['productQty']=newQtyValue;
		cartData['product'+ownerId]=productData;
		Cookies.set('cart',JSON.stringify(cartData));
	}
	else{
		console.log(false);
	}
	countCartItems()
}

function totalPriceCheckout(ownerId){
	priceValue=$('.priceValue'+'[ownerId='+ownerId+']').attr('value');
	productQty=$('.productQty'+'[ownerId='+ownerId+']').attr('value');
	if(productQty<=0){
		productQty=1;
	}
	productTotalPrice=parseFloat(parseFloat(priceValue)*parseInt(productQty)).toFixed(2);
	$('.productTotalPrice'+'[ownerId='+ownerId+']').text(productTotalPrice);
}

$('body').delegate('.nextQtyVal','click',function(){
	ownerId = $(this).attr('ownerId');
	console.log('nextQtyVal')
	var currentVal = $(this).attr('value');
	console.log(currentVal)
	newVal = parseInt(currentVal)+1;
	if (newVal<=0){
		newVal=1;
	}
	$(this).attr('value',newVal);
	qtyCheckout(ownerId,newVal);
	totalPriceCheckout(ownerId);
})

$('body').delegate('.prevQtyVal','click',function(){
	ownerId = $(this).attr('ownerId');
	var currentVal = $(this).attr('value');
	newVal = parseInt(currentVal)-1;
	if (newVal<=0){
		newVal=1;
	}
	$(this).attr('value',newVal);
	qtyCheckout(ownerId,newVal);
	totalPriceCheckout(ownerId);
})
$('body').delegate('.cartItemQty','click',function(){
	ownerId = $(this).attr('ownerId');
	var newVal = $(this).val();
	$(this).val(newVal);
	 
	qtyCheckout(ownerId,newVal);
	totalPriceCheckout(ownerId);
})

function prepareFormData(formFields,formId){
	var formData = {};
	function buildData(value){
		if ($('.'+value+formId).val() == ""){
			this.value = null;
		}
		else{
			formData[value] = $('.'+value+formId).val();
		}
	}
	formFields.forEach(buildData);
	return formData;
}

function checkoutCart(formData,url,type){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : type,
		url : url,
		success: function(response){
			if(response.status == 'added'){
				sweetAlert(title='',message=response.responseText,style='success');
				clearCart();
			}
			else{
				sweetAlert(title='',message=response.responseText,style='warning');
			}
		}
	})
}

function sweetAlert(title,message,style){
  swal(title,message,style);
}

function cartOperations(formData,url,type,responseForm,listName){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : type,
		url : url,
		success: function(response){
			if(response.status == 'added'){
				$('.'+listName).prepend(response[responseForm]);
				countCartItems();
			}
			else if(response.status=='removed'){
			}
			else{
				console.log('err');
				cartData={};
				Cookies.set('cart',JSON.stringify(cartData));
			}
		}
	})
}

function addItemsToCart(formData,url,responseForm,listName){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : 'POST',
		url : url,
		success: function(response){
			if(response.status=='added'){
				$('.'+listName).prepend(response[responseForm]);
			}
		}
	})
}
