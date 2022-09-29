resource_forms = [
	'resId',
	'resName',
	'resDesc',
	'resPrice',
	'resColor',
	'resSize',
]

/// getting the cookie data
$(document).ready(function () {
	cartCookie = Cookies.get('cart')
	if (cartCookie == undefined) {
		cartData = {}
	} else {
		cartData = JSON.parse(cartCookie)
		for (i in cartData) {
			ownerId = cartData[i]['resId']
			$('.add-to-cart' + '[ownerId=' + ownerId + ']')
				.addClass('added')
				.find('i')
				.addClass('ti-check')
				.removeClass('ti-shopping-cart')
				.siblings('span')
				.text(remove_from_cart_text)
			$('.productQty' + '[ownerId=' + ownerId + ']').val(
				cartData[i]['productQty'],
			)
			// $('.cartItemQty'+'[ownerId='+ownerId+']').val(cartData[i]["productQty"]);
			// $('.uiQtyText'+'[ownerId='+ownerId+']').text(cartData[i]["productQty"]);
		}
		for (i in cartData) {
			if (i) {
				var do_request = true
			}
		}
		if (do_request == true) {
			cartOperations(
				cartData,
				url_prefix + '/product/ui_cart/',
				'PUT',
				'htmlData',
				'cartItemsList',
			)
		}
	}
})

$('.wishlist-compare a').on('click', function (e) {
	e.preventDefault()
	ownerId = $(this).attr('ownerId')

	if ($(this).hasClass('added')) {
		removeFromWishlist(ownerId)
		$('.wishlist-compare a' + '[ownerId=' + ownerId + ']').removeClass('added')
	} else {
		addToWishlist(ownerId)
		$('.wishlist-compare a' + '[ownerId=' + ownerId + ']').addClass('added')
	}
})

$('body').delegate('.addToCart', 'click', function () {
	$(this).hide()
	ownerId = $(this).attr('ownerId')
	addToCart(ownerId)
	$('.add-to-cart' + '[ownerId=' + ownerId + ']')
		.addClass('added')
		.find('i')
		.addClass('ti-check')
		.removeClass('ti-shopping-cart')
		.siblings('span')
		.text(remove_from_cart_text)
})

$('body').delegate('.removeFromCart', 'click', function () {
	ownerId = $(this).attr('ownerId')
	removeFromCart(ownerId)
	$('.add-to-cart' + '[ownerId=' + ownerId + ']')
		.removeClass('added')
		.find('i')
		.removeClass('ti-check')
		.addClass('ti-shopping-cart')
		.siblings('span')
		.text(add_to_cart_text)
})

$('.add-to-cart').on('click', function (e) {
	e.preventDefault()
	ownerId = $(this).attr('ownerId')

	if ($(this).hasClass('added')) {
		removeFromCart(ownerId)
		$('.add-to-cart' + '[ownerId=' + ownerId + ']')
			.removeClass('added')
			.find('i')
			.removeClass('ti-check')
			.addClass('ti-shopping-cart')
			.siblings('span')
			.text(add_to_cart_text)
	} else {
		addToCart(ownerId)
		$('.add-to-cart' + '[ownerId=' + ownerId + ']')
			.addClass('added')
			.find('i')
			.addClass('ti-check')
			.removeClass('ti-shopping-cart')
			.siblings('span')
			.text(remove_from_cart_text)
	}
})

$('body').delegate('.checkoutCartBtn', 'click', function () {
	cartCookie = Cookies.get('cart')
	var data = {}
	var order_inv_lines = []
	cartData = JSON.parse(cartCookie)
	for (i in cartData) {
		var orderInvLine = {}
		orderInvLine['ResId'] = cartData[i]['resId']
		orderInvLine['OInvLineAmount'] = cartData[i]['productQty']
		orderInvLine['OInvLinePrice'] = cartData[i]['priceValue']
		order_inv_lines.push(orderInvLine)
	}

	data['OrderInvLines'] = order_inv_lines
	data['OInvDesc'] = $('.orderDesc').val()

	var PmId = 1
	// try {
	//	var payment_method = $('.paymentMethods input:checked')
	//	if (parseInt(payment_method[0].value) > 0){
	//		PmId = parseInt(payment_method[0].value)
	//	}
	// } catch {
	//	PmId = null;
	// }
	data['PmId'] = PmId
	data['PtId'] = 1
	checkoutCart(
		{ orderInv: data },
		url_prefix + '/commerce/checkout-cart-v1/',
		'POST',
	)
})

$('body').delegate('.sendReviewBtn', 'click', function (e) {
	e.preventDefault()
	ownerId = $(this).attr('ownerId')
	addRating(ownerId)
})

$('.rateButtons input').click(function () {
	$('.reviewRatingValue').val($(this).val())
})

function addRating(ownerId) {
	ratingValue = $('.reviewRatingValue').val()
	ratingRemark = $('.reviewRatingText').val()
	ratingRemark = ratingRemark.trim()
	productData = {
		resId: ownerId,
		ratingValue: ratingValue,
		ratingRemark: ratingRemark,
	}
	if (ratingRemark == '' || ratingValue == 0) {
		try {
			warningToaster((message = rating_message))
		} catch {
			warningToaster(
				(message = 'You should put your rating and write a review'),
			)
		}
	} else if (ratingRemark != '') {
		postData(
			(formData = productData),
			(url = url_prefix + '/product/ui_rating/'),
			(type = 'POST'),
			(formId = ownerId),
			(listName = null),
			(responseForm = null),
			(alertStyle = 'swal'),
		)
	}
}

function addToWishlist(ownerId) {
	productData = { resId: ownerId }
	postData(
		(formData = productData),
		(url = url_prefix + '/product/ui_wishlist/'),
		(type = 'POST'),
	)
	$('.addToWishlist' + '[ownerId=' + ownerId + ']').hide()
	$('.removeFromWishlist' + '[ownerId=' + ownerId + ']').show()
}

function removeFromWishlist(ownerId) {
	productData = { resId: ownerId }
	postData(
		(formData = productData),
		(url = url_prefix + '/product/ui_wishlist/'),
		(type = 'DELETE'),
	)
	$('.removeFromWishlist' + '[ownerId=' + ownerId + ']').hide()
	$('.addToWishlist' + '[ownerId=' + ownerId + ']').show()
}

function addToCart(ownerId) {
	$('.addToCart' + '[ownerId=' + ownerId + ']').hide()
	$('.removeFromCart' + '[ownerId=' + ownerId + ']').show()
	priceValue = parseFloat(
		$('.priceValue' + '[ownerId=' + ownerId + ']').attr('value'),
	)
	productQty = parseInt($('.productQty' + '[ownerId=' + ownerId + ']').val())
	pending_amount = parseInt(
		$('.productQty' + '[ownerId=' + ownerId + ']').attr('pending_amount'),
	)
	if (productQty > 1) {
	} else {
		productQty = 1
	}

	productData = {
		resId: ownerId,
		priceValue: priceValue,
		productQty: productQty,
	}
	cartData['product' + ownerId] = productData
	Cookies.set('cart', JSON.stringify(cartData))
	// sending request
	if (pending_amount > 0) {
		cartOperations(
			productData,
			url_prefix + '/product/ui_cart/',
			'POST',
			'htmlData',
			'cartItemsList',
		)
		qtyCheckout(ownerId, productQty, pending_amount)
		totalPriceCheckout(ownerId)
	} else {
		qtyCheckout(ownerId, productQty, pending_amount)
		totalPriceCheckout(ownerId)
		setTimeout(() => {
			$('.add-to-cart' + '[ownerId=' + ownerId + ']')
				// .removeClass('added')
				.find('i')
				.removeClass('ti-check')
				.addClass('ti-shopping-cart')
				.siblings('span')
				.text(add_to_cart_text)
		}, 100)
	}
}

function removeFromCart(ownerId) {
	if (ownerId > 0) {
		$('.cartObject' + ownerId).remove()
		$('.cartTableObject' + ownerId).remove()
		$('.removeFromCart' + '[ownerId=' + ownerId + ']').hide()
		$('.addToCart' + '[ownerId=' + ownerId + ']').show()
		delete cartData['product' + ownerId]
		Cookies.set('cart', JSON.stringify(cartData))
		countCartItems()
	} else {
		cartData = {}
		Cookies.set('cart', JSON.stringify(cartData))
		countCartItems()
	}
}

$('body').delegate('.clearCartBtn', 'click', function () {
	clearCart()
})

function clearCart() {
	cartCookie = Cookies.get('cart')
	if (cartCookie == undefined) {
		cartData = {}
	} else {
		cartData = JSON.parse(cartCookie)
		for (i in cartData) {
			ownerId = cartData[i]['resId']
			$('.cartObject' + ownerId).remove()
			$('.cartTableObject' + ownerId).remove()
			qtyCheckout(ownerId, (newQtyValue = 0))
			delete cartData['product' + ownerId]
			Cookies.set('cart', JSON.stringify(cartData))
			countCartItems()
		}
	}
}

function countCartItems() {
	var num = 0
	var totalPrice = 0
	var deliveryPrice = 0
	$('.cartItemsList li').each(function () {
		num += 1
	})
	for (i in cartData) {
		quantity = cartData[i]['productQty']
		price = cartData[i]['priceValue']
		totalPrice += price * quantity
		deliveryPrice += totalPrice + 20
	}
	$('.cartItemsFullQty').text(num)
	$('.cartTotalPrice').text(parseFloat(totalPrice).toFixed(2))
	$('.cartTotalPriceWithDelivery').text(parseFloat(deliveryPrice).toFixed(2))
}

function qtyCheckout(ownerId, newQtyValue, pending_amount = 0) {
	if (newQtyValue == 0) {
		removeFromCart(ownerId)
	}
	if (newQtyValue < 0) {
		newQtyValue = 1
	}

	if (pending_amount > 0) {
		if (newQtyValue >= 1) {
			if (newQtyValue > pending_amount) {
				if (pending_amount >= 1) {
					newQtyValue = pending_amount
					// warningToaster((message = qty_error_text))
				} else {
					newQtyValue = 1
				}
			}
		}
	} else {
		removeFromCart(ownerId)
		// warningToaster((message = qty_error_text))
	}

	$('.productQty' + '[ownerId=' + ownerId + ']').attr('value', newQtyValue)
	$('.productQty' + '[ownerId=' + ownerId + ']').text(newQtyValue)
	$('.cartItemQty' + '[ownerId=' + ownerId + ']').val(newQtyValue)
	$('.cartItemQty' + '[ownerId=' + ownerId + ']').text(newQtyValue)
	$('.uiQtyText' + '[ownerId=' + ownerId + ']').text(newQtyValue)
	if (cartData['product' + ownerId] != undefined) {
		productData = cartData['product' + ownerId]
		productData['productQty'] = newQtyValue
		cartData['product' + ownerId] = productData
		Cookies.set('cart', JSON.stringify(cartData))
	}
	// else{
	// 	console.log(false);
	// }
	countCartItems()
}

function totalPriceCheckout(ownerId) {
	priceValue = $('.priceValue' + '[ownerId=' + ownerId + ']').attr('value')
	productQty = $('.productQty' + '[ownerId=' + ownerId + ']').attr('value')
	if (productQty <= 0) {
		productQty = 1
	}
	productTotalPrice = parseFloat(
		parseFloat(priceValue) * parseInt(productQty),
	).toFixed(2)
	$('.productTotalPrice' + '[ownerId=' + ownerId + ']').text(productTotalPrice)
}

$('body').delegate('.cartItemQty', 'click', function () {
	var ownerId = $(this).find('input').attr('ownerId')
	var newVal = $(this).find('input').val()
	// $(this).val(newVal);
	var pending_amount = parseInt($(this).find('input').attr('pending_amount'))
	qtyCheckout(ownerId, newVal, pending_amount)
	totalPriceCheckout(ownerId)
})

function prepareFormData(formFields, formId) {
	var formData = {}
	function buildData(value) {
		if ($('.' + value + formId).val() == '') {
			this.value = null
		} else {
			formData[value] = $('.' + value + formId).val()
		}
	}
	formFields.forEach(buildData)
	return formData
}

function checkoutCart(formData, url, type) {
	$.ajax({
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify(formData),
		type: type,
		url: url,
		success: function (response) {
			if (response.status == 1) {
				swal(
					(title = ''),
					(message = response.responseText),
					(style = 'success'),
				)
				clearCart()
				// setTimeout(function(){
				// 	window.location.href = url_prefix+'/';
				// }, 5000);
			} else {
				swal(
					(title = ''),
					(message = response.responseText),
					(style = 'warning'),
				)
			}
		},
	})
}

function sendReview(formData, url, type, formId) {
	$.ajax({
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify(formData),
		type: type,
		url: url,
		success: function (response) {
			if (response.status == 'added') {
				swal(
					(title = ''),
					(message = response.responseText),
					(style = 'success'),
				)
				$('[ownerId=' + formId + ']').remove()
			} else {
				swal(
					(title = ''),
					(message = response.responseText),
					(style = 'warning'),
				)
			}
		},
	})
}

function cartOperations(formData, url, type, responseForm, listName) {
	$.ajax({
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify(formData),
		type: type,
		url: url,
		success: function (response) {
			if (response.status == 'added') {
				$('.' + listName).prepend(response[responseForm])
				countCartItems()
			} else if (response.status == 'removed') {
			} else {
				// console.log('err');
				cartData = {}
				Cookies.set('cart', JSON.stringify(cartData))
			}
		},
	})
}

function addItemsToCart(formData, url, responseForm, listName) {
	$.ajax({
		contentType: 'application/json',
		dataType: 'json',
		data: JSON.stringify(formData),
		type: 'POST',
		url: url,
		success: function (response) {
			if (response.status == 'added') {
				$('.' + listName).prepend(response[responseForm])
			}
		},
	})
}

$('body').delegate('.addToWishlist', 'click', function () {
	$(this).hide()
	ownerId = $(this).attr('ownerId')
	addToWishlist(ownerId)
})

$('body').delegate('.removeFromWishlist', 'click', function () {
	ownerId = $(this).attr('ownerId')
	removeFromWishlist(ownerId)
})
