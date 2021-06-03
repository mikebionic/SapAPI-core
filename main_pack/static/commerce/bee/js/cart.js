$(document).ready(function(){
	local_cart_data = get_local_data_by_name('cart');
	if (local_cart_data){
		for (i in local_cart_data){
			var ownerId = local_cart_data[i]["resId"];
			$('.add-to-cart'+'[ownerId='+ownerId+']').addClass('added').find('i').addClass('ti-check').removeClass('ti-shopping-cart').siblings('span').text(remove_from_cart_text);
			$('.productQty'+'[ownerId='+ownerId+']').val(local_cart_data[i]["productQty"]);
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
})