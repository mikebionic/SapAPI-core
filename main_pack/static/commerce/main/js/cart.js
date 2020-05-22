
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
		console.log(cartData)
		cartOperations(cartData,'/commerce/product/ui_cart_table/','PUT','htmlData','cartItemsTable');
	}
});
