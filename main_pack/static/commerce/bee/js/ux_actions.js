resource_forms = ['resId','resName','resDesc','resPrice','resColor','resSize']

// !!! TODO: change to use of formatting
function configure_UI_CartStates(data){
	for (i in data){
		var ownerId = data[i]["resId"];
		$('.add-to-cart'+'[ownerId='+ownerId+']').addClass('added').find('i').addClass('ti-check').removeClass('ti-shopping-cart').siblings('span').text(remove_from_cart_text);
		$('.productQty'+'[ownerId='+ownerId+']').val(data[i]["productQty"]);
	}
}

//// Wishlist
$('.wishlist-compare a').on('click', function(e){
	e.preventDefault();
	var ownerId = $(this).attr('ownerId');

	if($(this).hasClass('added')){
		removeFromWishlist(ownerId);
		$('.wishlist-compare a'+'[ownerId='+ownerId+']').removeClass('added');
	} else {
		addToWishlist(ownerId);
		$('.wishlist-compare a'+'[ownerId='+ownerId+']').addClass('added');
	}
});

$('body').delegate('.addToWishlist','click',function(){
	$(this).hide();
	var ownerId = $(this).attr('ownerId');
	addToWishlist(ownerId);
})

$('body').delegate('.removeFromWishlist','click',function(){
	var ownerId = $(this).attr('ownerId');
	removeFromWishlist(ownerId);
});

function addToWishlist(ownerId){
	configure_wishlist(ownerId, "POST");
	$('.addToWishlist'+'[ownerId='+ownerId+']').hide();
	$('.removeFromWishlist'+'[ownerId='+ownerId+']').show();
}

function removeFromWishlist(ownerId){
	configure_wishlist(ownerId, "DELETE");
	$('.removeFromWishlist'+'[ownerId='+ownerId+']').hide();
	$('.addToWishlist'+'[ownerId='+ownerId+']').show();
}
///// wishlist

//// rating
$('body').delegate('.sendReviewBtn','click',function(e){
	e.preventDefault();
	var ownerId = $(this).attr('ownerId');
	addRating(ownerId);
});

$('.rateButtons input').click(function(){
	$('.reviewRatingValue').val($(this).val());
})

function addRating(ownerId){
	var ratingValue = $('.reviewRatingValue').val();
	var ratingRemark = $('.reviewRatingText').val();
	configure_rating(ownerId, ratingValue, ratingRemark);
}
//// rating


//// cart actions
$('body').delegate('.removeFromCart','click',function(){
	var ownerId = $(this).attr('ownerId');
	removeFromCart(ownerId, table_object=true);
	qtyCheckout(ownerId, newQtyValue = 0);
});


$('body').delegate('.clearCartBtn','click',function(){
	clearCart();
});


$('body').delegate('.cartItemQty','click',function(){
	var ownerId = $(this).parent().find('input').attr('ownerId');
	var newVal = $(this).parent().find('input').attr('value');
	var pending_amount = parseInt($(this).parent().find('input').attr('pending_amount'));
	var min_amount = parseInt($(this).parent().find('input').attr('min_amount'));
	var max_amount = parseInt($(this).parent().find('input').attr('max_amount'));

	if (newVal < min_amount){
		newVal = 1;
		qtyCheckout(ownerId, newVal, min_amount, max_amount, pending_amount);
	}
	else {
		qtyCheckout(ownerId, newVal, min_amount, max_amount, pending_amount);
	}
	totalPriceCheckout(ownerId);
})


// /*-- Quantity  -*/     //???????????
// $('body').delegate('.qtybtn','click', function() {
// 	$button = $(this);

// 	var ownerId = $(this).parent().find('input').attr('ownerId');
// 	var addToCartButton = $('.add-to-cart'+'[ownerId='+ownerId+']');
// 	var qtySelectWrapper = addToCartButton.parent().find('.cartItemQty');

// 	var current_qty_wrapper = $button.parent();
// 	var oldValue = current_qty_wrapper.find('input').val();
// 	if (oldValue < 1) {
// 		oldValue = 1;
// 	}

// 	if ($button.hasClass('qtyplus')) {
// 	  var newVal = parseFloat(oldValue) + 1;
// 	} 

// 	else {
// 		if (oldValue > 1) {
// 			var newVal = parseFloat(oldValue) - 1;
// 		}
// 		else {
// 			newVal = 1;
// 			removeFromCart(ownerId)
// 			qtySelectWrapper.hide()
// 			addToCartButton.show()
// 		}
// 	}
// 	$(this).parent().find('input').val(newVal);
// 	qtySelectWrapper.find('input').val(newVal);
// });

/// Add to Cart and other cart actions
$('body').delegate('.add-to-cart', 'click', function() {
	var ownerId = $(this).attr('ownerId');
	if($(this).hasClass('added')){
		removeFromCart(ownerId);
		$('.add-to-cart'+'[ownerId='+ownerId+']').removeClass('added').find('i').removeClass('ti-check').addClass('ti-shopping-cart').siblings('span').text(add_to_cart_text);
	} else{
		addToCart(ownerId);
		$('.add-to-cart'+'[ownerId='+ownerId+']').addClass('added').find('i').addClass('ti-check').removeClass('ti-shopping-cart').siblings('span').text(remove_from_cart_text);
	}
})


$('body').delegate('.productQty', 'keyup', function() {
	var ownerId = $(this).attr('ownerid');
	var this_quantity = parseInt($(this).val());
	var pending_amount = parseInt($(this).attr('pending_amount'))
	var min_amount = parseInt($(this).attr('min_amount'))
	var max_amount = parseInt($(this).attr('max_amount'))

	if (this_quantity >= 1) {}
	else {
		this_quantity = 1;
		removeFromCart(ownerId)
	}
	qtyCheckout(ownerId, this_quantity, min_amount, max_amount, pending_amount);
	totalPriceCheckout(ownerId);
})
//// ????????????
function addToCart(ownerId){
	var priceValue = parseFloat($('.priceValue'+'[ownerId='+ownerId+']').attr('value'));
	var productQty = parseInt($('.productQty'+'[ownerId='+ownerId+']').val());
	var pending_amount = parseInt($('.productQty'+'[ownerId='+ownerId+']').attr('pending_amount'));
	var min_amount = parseInt($('.productQty'+'[ownerId='+ownerId+']').attr('min_amount'));
	var max_amount = parseInt($('.productQty'+'[ownerId='+ownerId+']').attr('max_amount'));

	configure_adding_to_cart(
		ownerId,
		priceValue,
		productQty,
		pending_amount,
		min_amount,
		max_amount);
}

function UI_cart_removal(ownerId){
	$('.add-to-cart'+'[ownerId='+ownerId+']').removeClass('added').find('i').removeClass('ti-check').addClass('ti-shopping-cart').siblings('span').text(add_to_cart_text);
	// var addToCartButton = $('.add-to-cart'+'[ownerId='+ownerId+']');
	// var qtySelectWrapper = addToCartButton.parent().find('.cartItemQty');
	// qtySelectWrapper.hide();
	// addToCartButton.show();
}

function totalPriceCheckout(ownerId){
	var priceValue = $('.priceValue'+'[ownerId='+ownerId+']').attr('value');
	var productQty = $('.productQty'+'[ownerId='+ownerId+']').attr('value');
	if(productQty <= 0){
		productQty = 1;
	}
	var productTotalPrice = parseFloat(parseFloat(priceValue)*parseInt(productQty)).toFixed(2);
	$('.productTotalPrice'+'[ownerId='+ownerId+']').text(productTotalPrice);
}

function removeFromCart(ownerId, table_object = false){
	if(ownerId > 0){
		$(`.cartObject${ownerId}`).remove();
		if (table_object === true){
			$(`.cartTableObject${ownerId}`).remove();
		}
	}
	configure_cart_removal(ownerId)
}

function clearCart(){
	var local_cart_data = get_local_data_by_name();
	if (local_cart_data){
		for (i in local_cart_data){
			var ownerId = local_cart_data[i]["resId"];

			$(`.cartObject${ownerId}`).remove();
			$(`.cartTableObject${ownerId}`).remove();

			qtyCheckout(ownerId, newQtyValue = 0)
			delete local_cart_data[`product${ownerId}`];
			set_local_data_by_name('cart', local_cart_data)
			countCartItems();
		}
	}
}

function qtyCheckout(
	ownerId,
	qtyValue,
	min_amount = 0,
	max_amount = 0,
	pending_amount = 0){

	var qtyValue = configure_qty_checkout(
		ownerId,
		qtyValue,
		min_amount,
		max_amount,
		pending_amount);

	$('.productQty'+'[ownerId='+ownerId+']').attr('value',qtyValue);
	$('.productQty'+'[ownerId='+ownerId+']').text(qtyValue);
	$('.productQty'+'[ownerId='+ownerId+']').val(qtyValue);
	$('.cartItemQty'+'[ownerId='+ownerId+']').val(qtyValue);
	$('.cartItemQty'+'[ownerId='+ownerId+']').text(qtyValue);
	$('.uiQtyText'+'[ownerId='+ownerId+']').text(qtyValue);
}

function countCartItems(){
	var totalNum = 0;
	var totalPrice = 0;
	cart_qty_data = configure_cart_item_count();
	if (cart_qty_data){
		totalNum = cart_qty_data["totalNum"];
		totalPrice = cart_qty_data["totalPrice"];
	}
	$('.cartItemsFullQty').text(totalNum);
	$('.cartTotalPrice').text(parseFloat(totalPrice).toFixed(2));
	$('.cartTotalPrice').val(parseFloat(totalPrice).toFixed(2));
}
//////////////////////////////


/// // payment stuff
// $('.paymentMethods input').click(function () {
// 	data2 = $('.cartItemsTable')[0]
// 	if (data2.innerText != ""){
// 		$('.checkoutForm').show();
// 	}
// })


$('body').delegate('.checkoutCartBtn','click',function(){
	var data = collectOrderData()
	data['OInvDesc'] = $('.orderDesc').val();
	data['PmId'] = 1
	data['PtId'] = 1

	var order_data = {"orderInv": data, "validated": false}
	set_local_data_by_name('orderInv', order_data)
	checkoutCart(order_data ,`${url_prefix}/checkout-cart-v1/`,'POST');
});
