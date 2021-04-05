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
			$('.add-to-cart'+'[ownerId='+ownerId+']').hide();
			$('.add-to-cart'+'[ownerId='+ownerId+']').parent().find('.cartItemQty').show();
			$('.productQty'+'[ownerId='+ownerId+']').val(cartData[i]["productQty"]);
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

$('.wishlist-compare a').on('click', function(e){
	e.preventDefault();
	ownerId = $(this).attr('ownerId');

	if($(this).hasClass('added')){
		removeFromWishlist(ownerId);
		$('.wishlist-compare a'+'[ownerId='+ownerId+']').removeClass('added');
	} else{
		addToWishlist(ownerId);
		$('.wishlist-compare a'+'[ownerId='+ownerId+']').addClass('added');
	}
});


$('body').delegate('.removeFromCart','click',function(){
	ownerId = $(this).attr('ownerId');
	removeFromCart(ownerId, table_object=true);
});


$('body').delegate('.checkoutCartBtn','click',function(){
	cartCookie = Cookies.get('cart');
	data={}
	cartData=JSON.parse(cartCookie);
	data['cartData']=cartData;
	data['orderDesc']=$('.orderDesc').val();
	checkoutCart(data,url_prefix+'/product/ui_cart_checkout/','POST');
});


$('body').delegate('.sendReviewBtn','click',function(e){
	e.preventDefault();
	ownerId = $(this).attr('ownerId');
	addRating(ownerId);
});


$('.rateButtons input').click(function(){
	$('.reviewRatingValue').val($(this).val());
})

function addRating(ownerId){
	ratingValue = $('.reviewRatingValue').val();
	ratingRemark = $('.reviewRatingText').val();
	ratingRemark = ratingRemark.trim()
	productData={
		'resId':ownerId,
		'ratingValue':ratingValue,
		'ratingRemark':ratingRemark
	};
	if (ratingRemark != ""){
		postData(formData=productData,url=url_prefix+"/product/ui_rating/",type="POST",formId=ownerId,listName=null,responseForm=null,alertStyle="swal")
	}
}

function addToWishlist(ownerId){
	productData={'resId':ownerId};
	postData(formData=productData,url=url_prefix+"/product/ui_wishlist/",type="POST");
	$('.addToWishlist'+'[ownerId='+ownerId+']').hide();
	$('.removeFromWishlist'+'[ownerId='+ownerId+']').show();
}

function removeFromWishlist(ownerId){
	productData={'resId':ownerId};
	postData(formData=productData,url=url_prefix+"/product/ui_wishlist/",type="DELETE");
	$('.removeFromWishlist'+'[ownerId='+ownerId+']').hide();
	$('.addToWishlist'+'[ownerId='+ownerId+']').show();
}

function addToCart(ownerId){	
	// $('.addToCart'+'[ownerId='+ownerId+']').hide();
	// $('.removeFromCart'+'[ownerId='+ownerId+']').show();
	priceValue = $('.priceValue'+'[ownerId='+ownerId+']').attr('value');
	productQty = $('.productQty'+'[ownerId='+ownerId+']').val();
	pending_amount = $('.productQty'+'[ownerId='+ownerId+']').attr('pending_amount');
	if(productQty > 1){} else {
		productQty = 1;
	}
	// saving cookie
	productData={'resId':ownerId,'priceValue':priceValue,'productQty':productQty};
	cartData['product'+ownerId]=productData;
	Cookies.set('cart',JSON.stringify(cartData));
	// sending request
	if (pending_amount > 0){
		cartOperations(productData,url_prefix+'/product/ui_cart/','POST','htmlData','cartItemsList');
		qtyCheckout(ownerId,productQty,pending_amount);
		totalPriceCheckout(ownerId)
	}
	else {
		qtyCheckout(ownerId,productQty,pending_amount);
		totalPriceCheckout(ownerId)
	}
}

function removeFromCart(ownerId, table_object = false){
	if(ownerId > 0){
		$('.cartObject'+ownerId).remove();
		if (table_object === true){
			$('.cartTableObject'+ownerId).remove();
		}
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

function qtyCheckout(ownerId,newQtyValue,pending_amount = 0){
	// if(newQtyValue <= 0){
	// 	newQtyValue = 1;
	// };
	if (pending_amount > 0){
		if (newQtyValue >= 1){
			if (newQtyValue > pending_amount){
				if(pending_amount >= 1){
					newQtyValue = pending_amount;
					warningToaster(message = qty_error_text);
				}
				else {
					newQtyValue = 1;
				}
			}
		}
	}
	else {
		var addToCartButton = $('.add-to-cart'+'[ownerId='+ownerId+']')
		var qtySelectWrapper = addToCartButton.parent().find('.cartItemQty')
		removeFromCart(ownerId)
		qtySelectWrapper.hide()
		addToCartButton.show()
		warningToaster(message = qty_error_text);
	}

	$('.productQty'+'[ownerId='+ownerId+']').attr('value',newQtyValue);
	$('.productQty'+'[ownerId='+ownerId+']').text(newQtyValue);
	$('.productQty'+'[ownerId='+ownerId+']').val(newQtyValue);
	$('.cartItemQty'+'[ownerId='+ownerId+']').val(newQtyValue);
	$('.cartItemQty'+'[ownerId='+ownerId+']').text(newQtyValue);
	$('.uiQtyText'+'[ownerId='+ownerId+']').text(newQtyValue);
	if(cartData['product'+ownerId]!=undefined){
		productData = cartData['product'+ownerId];
		productData['productQty']=newQtyValue;
		cartData['product'+ownerId]=productData;
		Cookies.set('cart',JSON.stringify(cartData));
	}
	// else{
	// 	console.log(false);
	// }
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

$('body').delegate('.cartItemQty','click',function(){
	var ownerId = $(this).find('input').attr('ownerId');
	var newVal = $(this).find('input').val();
	var pending_amount = parseInt($(this).find('input').attr('pending_amount'))
	qtyCheckout(ownerId,newVal,pending_amount);
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
				setTimeout(function(){
					window.location.href = url_prefix+'/orders';
				}, 5000);
			}
			else{
				sweetAlert(title='',message=response.responseText,style='warning');
			}
		}
	})
}

function sendReview(formData,url,type,formId){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : type,
		url : url,
		success: function(response){
			if(response.status == 'added'){
				sweetAlert(title='',message=response.responseText,style='success');
				$('[ownerId='+formId+']').remove();
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
				// console.log('err');
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


$('body').delegate('.addToWishlist','click',function(){
	$(this).hide();
	ownerId = $(this).attr('ownerId');
	addToWishlist(ownerId);
})

$('body').delegate('.removeFromWishlist','click',function(){
	ownerId = $(this).attr('ownerId');
	removeFromWishlist(ownerId);
});


/*-- Quantity  -*/
$('body').delegate('.qtybtn','click', function() {
	$button = $(this);

	var ownerId =  $(this).parent().find('input').attr('ownerId');
	var addToCartButton = $('.add-to-cart'+'[ownerId='+ownerId+']')
	var qtySelectWrapper = addToCartButton.parent().find('.cartItemQty')

	var current_qty_wrapper = $button.parent()
	var oldValue = current_qty_wrapper.find('input').val();
	if (oldValue < 1) {
		oldValue = 1;
	}
	if ($button.hasClass('qtyplus')) {
	  var newVal = parseFloat(oldValue) + 1;
	} else {
	   // Don't allow decrementing below zero
	  if (oldValue > 1) {
			var newVal = parseFloat(oldValue) - 1;
		}
		else {
			newVal = 1;
			removeFromCart(ownerId)
			qtySelectWrapper.hide()
			addToCartButton.show()
	  }
	}
	$(this).parent().find('input').val(newVal);
	qtySelectWrapper.find('input').val(newVal);
});


$('body').delegate('.add-to-cart', 'click', function() {
	var ownerId = $(this).attr('ownerId');
	var all_this = $('.add-to-cart'+'[ownerId='+ownerId+']')
	all_this.hide()
	var qty_obj = all_this.parent().find('.cartItemQty')
	qty_obj.show();
	var qtyvalue = all_this.parent().find('input').val();
	if (qtyvalue < 1) {
		all_this.parent().find('input').val(1)
	}
	addToCart(ownerId);
})


$('body').delegate('.productQty', 'keyup', function() {
	var ownerId = $(this).attr('ownerid');
	var all_this = $('.productQty'+'[ownerId='+ownerId+']')
	var qtySelectWrapper = all_this.parent()
	
	var this_quantity = parseInt($(this).val());
	var pending_amount = parseInt($(this).attr('pending_amount'))
	var addToCartButton = qtySelectWrapper.parent().find('.add-to-cart')
	if (this_quantity >= 1) {}
	else {
		this_quantity = 1;
		removeFromCart(ownerId)
		qtySelectWrapper.hide()
		addToCartButton.show()
	}
	qtyCheckout(ownerId, this_quantity, pending_amount);
	totalPriceCheckout(ownerId);
	// qtySelectWrapper.find('input').val(this_quantity);
})
