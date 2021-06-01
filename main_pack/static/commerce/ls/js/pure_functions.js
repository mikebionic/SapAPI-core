
function get_local_data_by_name(data_name = 'cart', parse_json = true){
	var local_data = localStorage.getItem(data_name);
	if(local_data == undefined){
		data = {};
	}
	else{
		data = parse_json ? JSON.parse(local_data) : local_data;
	}
	return data
}

function set_local_data_by_name(data_name, data_payload, stringify_json = true){
	if (data_payload){
		data_payload = stringify_json ? JSON.stringify(data_payload) : data_payload; 
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
		}
	})
}



function checkoutCart(formData, url, type){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type: type,
		url: url,
		success: function(response){
			if(response.status == 1){
				sweetAlert(title='', message=response.responseText, style='success');
				clearCart();
				setTimeout(function(){
					window.location.href = url_prefix+'/orders';
				}, 5000);
			}
			else{
				sweetAlert(title='', message=response.responseText, style='warning');
			}
		}
	})
}


function sendReview(formData, url, type, formId){
	$.ajax({
		contentType:"application/json",
		dataType:"json",
		data:JSON.stringify(formData),
		type : type,
		url : url,
		success: function(response){
			if(response.status == 'added'){
				sweetAlert(title='', message=response.responseText, style='success');
				$('[ownerId='+formId+']').remove();
			}
			else{
				sweetAlert(title='', message=response.responseText, style='warning');
			}
		}
	})
}


function addItemsToCart(formData, url, responseForm, listName){
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

