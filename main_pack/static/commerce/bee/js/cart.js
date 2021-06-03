$(document).ready(function(){
	cartCookie = Cookies.get('cart');
	if(cartCookie==undefined){
		cartData={};
	}
	else{
		cartData=JSON.parse(cartCookie);
		for (i in cartData){
			ownerId = cartData[i]["resId"];
			$('.add-to-cart'+'[ownerId='+ownerId+']').addClass('added').find('i').addClass('ti-check').removeClass('ti-shopping-cart').siblings('span').text(remove_from_cart_text);
			$('.productQty'+'[ownerId='+ownerId+']').val(cartData[i]["productQty"]);
			// $('.cartItemQty'+'[ownerId='+ownerId+']').val(cartData[i]["productQty"]);
			// $('.uiQtyText'+'[ownerId='+ownerId+']').text(cartData[i]["productQty"]);
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
