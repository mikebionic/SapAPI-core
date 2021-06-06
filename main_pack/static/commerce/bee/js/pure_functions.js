
function get_local_data_by_name(data_name = 'cart', parse_json = true){
	var local_data = localStorage.getItem(data_name);
	if(local_data == undefined){
		data = {};
	}
	else{
		data = parse_json ? JSON.parse(local_data):local_data;
	}
	return data
}

function set_local_data_by_name(data_name, data_payload, stringify_json = true){
	if (data_payload){
		data_payload = stringify_json ? JSON.stringify(data_payload):data_payload; 
		localStorage.setItem(data_name, data_payload);
		return true
	}
	return false
}


function handle_missing_image_errors(){
	var no_image_src;
	try {
		no_image_src = no_photo_errorhandler_image;
	}
	catch{
		no_image_src = ''
	}
	document.addEventListener('error', function (event) {
		if (event.target.tagName.toLowerCase() !== 'img') return;
		event.target.src = no_image_src;
		// event.target.className = 'full-width'
		// event.target.style = "padding: 45px";
	}, true);
}


function collectOrderData(){
	var local_cart_data = get_local_data_by_name('cart');
	var data = {}
	var order_inv_lines = []
	for (i in local_cart_data){
		var orderInvLine = {}
		orderInvLine["ResId"] = local_cart_data[i]["resId"]
		orderInvLine["OInvLineAmount"] = local_cart_data[i]["productQty"]
		orderInvLine["OInvLinePrice"] = local_cart_data[i]["priceValue"]
		order_inv_lines.push(orderInvLine)
	}
	data['OrderInvLines'] = order_inv_lines;
	return data
}


function sweetAlert(title, message, style){
  swal(title, message, style);
}


function makeCartRequests(
	payload_data,
	url,
	type,
	responseForm,
	listName){
	$.ajax({
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(payload_data),
		type: type,
		url: url,
		success: function(response){
			if(response.status == 'added'){
				$(`.${listName}`).prepend(response[responseForm]);
				countCartItems();
			}
			else if(response.status == 'removed'){}
			else{
				set_local_data_by_name('cart', {})
			}
		},
		error: function(){
			errorToaster(message = unknown_error_text);
		}
	})
}


function checkoutCart(payload_data, url, type){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data: JSON.stringify(payload_data),
		type: type,
		url: url,
		success: function(response){
			if(response.status == 1){
				swal(title='', message=response.responseText, style='success');
				clearCart();
				setTimeout(function(){
					window.location.href = `${url_prefix}/orders`;
				}, 5000);
			}
			else{
				swal(title='', message=response.responseText, style='warning');
			}
		},
		error: function(){
			swal(title='', message=unknown_error_text, style='warning');
		}
	})
}


function sendReview(payload_data, url, type, formId){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(payload_data),
		type:type,
		url:url,
		success: function(response){
			if(response.status == 'added'){
				swal(title='', message=response.responseText, style='success');
				$('[ownerId='+formId+']').remove();
			}
			else{
				swal(title='', message=response.responseText, style='warning');
			}
		},
		error: function(){
			errorToaster(message = unknown_error_text);
		}
	})
}


function addItemsToCart(payload_data, url, responseForm, listName){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(payload_data),
		type:'POST',
		url:url,
		success: function(response){
			if(response.status=='added'){
				$('.'+listName).prepend(response[responseForm]);
				successToaster(message = success_title);
			}
		},
		error: function(){
			errorToaster(message = unknown_error_text);
		}
	})
}


function configure_adding_to_cart(
	ownerId,
	priceValue,
	productQty,
	pending_amount,
	min_amount,
	max_amount){
	if(productQty > 1){} else {productQty = 1;}

	if (min_amount > 0){
		if (productQty < min_amount){
			productQty = min_amount;
		}
	}
	if (min_amount > 0){
		if (productQty > max_amount){
			productQty = max_amount;
		}
	}
	if (pending_amount > 0 && productQty > pending_amount && pending_amount < max_amount){
		productQty = pending_amount;
	}

	productQty = parseInt(productQty)
	productData={'resId':ownerId,'priceValue':priceValue,'productQty':productQty};


	local_cart_data = get_local_data_by_name();
	local_cart_data['product' + ownerId] = productData;
	set_local_data_by_name('cart', local_cart_data)

	if (pending_amount > 0){
		makeCartRequests(
			productData,
			`${url_prefix}/product/ui_cart/`,
			'POST',
			'htmlData',
			'cartItemsList');
	}
	qtyCheckout(ownerId, productQty, min_amount, max_amount, pending_amount);
	totalPriceCheckout(ownerId)
}


$(document).ready(function(){
	var do_ajax_request = false;
	var local_cart_data = get_local_data_by_name('cart');
	var local_currency_data = get_local_data_by_name('currency_code', parse_json = false);

	if(local_cart_data == undefined || local_currency_data != session_currency_code){
		local_cart_data = {};
		set_local_data_by_name('cart', local_cart_data)
	}
	if (local_cart_data){
		configure_UI_CartStates(local_cart_data);
		for (i in local_cart_data){
			if (i){
				do_ajax_request = true;
			}
		}
		if (do_ajax_request == true){
			makeCartRequests(
				local_cart_data,
				`${url_prefix}/product/ui_cart/`,
				'PUT',
				'htmlData',
				'cartItemsList'
			);
		}
	}

	set_local_data_by_name('currency_code', session_currency_code, stringify_json = false);
});

function configure_wishlist(ownerId, type){
	var productData={'resId':ownerId};
	postData(payload_data=productData,url=`${url_prefix}/product/ui_wishlist/`,type=type);
}

function configure_rating(ownerId, ratingValue, ratingRemark){
	ratingRemark = ratingRemark.trim()
	var productData = {
		'resId': ownerId,
		'ratingValue': ratingValue,
		'ratingRemark': ratingRemark
	};
	if (ratingRemark == "" || ratingValue == 0){
		try {
			warningToaster(message = rating_message);
		}
		catch {
			warningToaster(message = "You should put your rating and write a review");
		}
	}
	else if (ratingRemark != ""){
		postData(payload_data=productData,url=`${url_prefix}/product/ui_rating/`,type="POST",formId=ownerId,listName=null,responseForm=null,alertStyle="swal")
	}
}

function prepareFormData(formFields,formId){
	var formData = {};
	function buildData(value){
		if ($(`.${value}${formId}`).val() == ""){
			this.value = null;
		}
		else{
			formData[value] = $(`.${value}${formId}`).val();
		}
	}
	formFields.forEach(buildData);
	return formData;
}

function configure_cart_removal(ownerId){
	if (ownerId > 0){
		var local_cart_data = get_local_data_by_name();
		delete local_cart_data['product'+ownerId];
		set_local_data_by_name('cart', local_cart_data);
		countCartItems();
	}
	else {
		var local_cart_data = {};
		set_local_data_by_name('cart', local_cart_data);
		countCartItems();
	}
}

function configure_qty_checkout(
	ownerId,
	qtyValue,
	min_amount = 0,
	max_amount = 0,
	pending_amount = 0
){
	if (pending_amount > 0){
		if (min_amount > 0){
			if (qtyValue < min_amount){
				qtyValue = min_amount;
			}
		}
		if (max_amount > 0){
			if (qtyValue > max_amount){
				qtyValue = max_amount;
				warningToaster(message = qty_error_text);
			}
		}
		if (pending_amount > 0 && qtyValue > pending_amount){
			if(pending_amount < max_amount && max_amount > 0 || max_amount == 0){
				qtyValue = pending_amount;
				warningToaster(message = qty_error_text);
			}
		}
	}

	else {
		UI_cart_removal(ownerId)
		removeFromCart(ownerId)
	}

	qtyValue = parseInt(qtyValue);

	var local_cart_data = get_local_data_by_name();

	if(local_cart_data[`product${ownerId}`] != undefined){
		var productData = local_cart_data[`product${ownerId}`];
		productData['productQty'] = qtyValue;
		local_cart_data[`product${ownerId}`] = productData;
		set_local_data_by_name('cart', local_cart_data);
	}
	countCartItems();

	return qtyValue
}

function configure_cart_item_count(){
	var totalPrice = 0;
	var totalNum = 0;
	var local_cart_data = get_local_data_by_name();

	for(i in local_cart_data){
		quantity = local_cart_data[i]['productQty'];
		price = local_cart_data[i]['priceValue'];
		totalPrice += price * quantity;
		totalNum += 1;
	}
	var res = {
			"totalNum": totalNum,
			"totalPrice": totalPrice,
	}
	return res;
}
