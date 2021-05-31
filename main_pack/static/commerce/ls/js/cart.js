$(document).ready(function(){
	// cartCookie = Cookies.get('cart');
	cartData = get_local_data_by_name();
	// console.log(cartData)
	if (cartData){
		for (i in cartData){
			ownerId = cartData[i]["resId"];
			$('.addToCart'+'[ownerId='+ownerId+']').hide();
			$('.removeFromCart'+'[ownerId='+ownerId+']').show();
			$('.productQty'+'[ownerId='+ownerId+']').val(cartData[i]["productQty"]);
			$('.uiQtyText'+'[ownerId='+ownerId+']').text(cartData[i]["productQty"]);
			totalPriceCheckout(ownerId);
		}
		cartOperations(cartData,url_prefix+'/product/ui_cart_table/','PUT','htmlData','cartItemsTable');
	}
});