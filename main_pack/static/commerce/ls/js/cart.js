$(document).ready(function(){
	local_cart_data = get_local_data_by_name('cart');
	if (local_cart_data){
		for (i in local_cart_data){
			ownerId = local_cart_data[i]["resId"];
			$('.addToCart'+'[ownerId='+ownerId+']').hide();
			$('.removeFromCart'+'[ownerId='+ownerId+']').show();
			$('.productQty'+'[ownerId='+ownerId+']').val(local_cart_data[i]["productQty"]);
			$('.uiQtyText'+'[ownerId='+ownerId+']').text(local_cart_data[i]["productQty"]);
			totalPriceCheckout(ownerId);
		}
		makeCartRequests(
			local_cart_data,
			`${url_prefix}/product/ui_cart_table/`,
			'PUT',
			'htmlData',
			'cartItemsTable'
		);
	}
});

$(document).ready(function(){
	set_local_data_by_name('orderInv', {});
})