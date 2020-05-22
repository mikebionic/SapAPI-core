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
		}
		cartOperations(cartData,'/commerce/product/ui_cart/','PUT','htmlData','cartItemsList');
	}
});


$('body').delegate('.addToCart','click',function(){
	$(this).hide();
	ownerId = $(this).attr('ownerId');
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
	cartOperations(productData,'/commerce/product/ui_cart/','POST','htmlData','cartItemsList');
	totalPriceCheckout(ownerId)
	qtyCheckout(ownerId,productQty);
})

$('body').delegate('.removeFromCart','click',function(){
	ownerId = $(this).attr('ownerId');
	console.log(ownerId)
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
});

$('body').delegate('.clearCartBtn','click',function(){
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
	
});

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
	$('.cartItemsQty').text(num);
	$('.cartTotalPrice').text(totalPrice);
}


function qtyCheckout(ownerId,newQtyValue){
	$('.productQty'+'[ownerId='+ownerId+']').val(newQtyValue);
	if(cartData['product'+ownerId]!=undefined){
		productData = cartData['product'+ownerId];
		productData['productQty']=newQtyValue;
		cartData['product'+ownerId]=productData;
		Cookies.set('cart',JSON.stringify(cartData));
		console.log(cartData)
	}
	else{
		console.log(false);
	}
	countCartItems()
}

function totalPriceCheckout(ownerId){
	priceValue=$('.priceValue'+'[ownerId='+ownerId+']').attr('value');
	productQty=$('.productQty'+'[ownerId='+ownerId+']').val();
	if(productQty>1){}else{
		productQty=1;
	}
	productTotalPrice=priceValue*productQty;
	$('.productTotalPrice'+'[ownerId='+ownerId+']').text(productTotalPrice);
}

$('body').delegate('.productQty','click',function(){
	ownerId = $(this).attr('ownerId');
	newQtyValue = $(this).val(); 
	console.log(newQtyValue)
	qtyCheckout(ownerId,newQtyValue);
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
				console.log('removed-ok');
			}
			else{
				console.log('err');
				console.log(response);
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
