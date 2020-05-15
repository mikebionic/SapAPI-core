resource_forms = ['resId','resName','resDesc','resPrice','resColor','resSize']

/// getting the cookie data
$(document).ready(function(){
	cartCookie = Cookies.get('cart');
	if(cartCookie==undefined){
		cartData={};
		console.log('it was undefined');
	}
	else{
		cartData=JSON.parse(cartCookie);
		console.log(cartData)
		for (i in cartData){
			ownerId = cartData[i]["resId"];
			$('.addToCart'+'[ownerId='+ownerId+']').hide();
			$('.removeFromCart'+'[ownerId='+ownerId+']').show();
		}
		cartOperations(cartData,'/commerce/product/ui_cart/','PUT','htmlData','cartItemsList');
	}
});


$('body').delegate('.addToCart','click',function(){
	$(this).hide();
	ownerId = $(this).attr('ownerId');
	$('.removeFromCart'+'[ownerId='+ownerId+']').show();
	productData={'resId':ownerId};
	cartData['product'+ownerId]=productData;
	Cookies.set('cart',JSON.stringify(cartData));
	cartOperations(productData,'/commerce/product/ui_cart/','POST','htmlData','cartItemsList');
})

$('body').delegate('.removeFromCart','click',function(){
	ownerId = $(this).attr('ownerId');
	$('.cartObject'+ownerId).remove();
	$('.removeFromCart'+'[ownerId='+ownerId+']').hide();
	$('.addToCart'+'[ownerId='+ownerId+']').show();
	delete cartData['product'+ownerId];
	Cookies.set('cart',JSON.stringify(cartData));
	countCartItems();
})

	// $('.cartItemsQty').text(itemNum);
function countCartItems(){
	var num=0;
	$('.cartItemsList li').each(function(){
		num+=1;
	});
	$('.cartItemsQty').text(num);
}

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
			if(response.status=='removed'){
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
