
$('body').delegate('.productQty','change',function(){
	ownerId = $(this).attr('ownerId');
	totalPriceCheck(ownerId);
})

$('body').delegate('.productPrice','change',function(){
	ownerId = $(this).attr('ownerId');
	totalPriceCheck(ownerId);
})
// calculation functions 
function totalPriceCheck(ownerId){
	productPrice=$('.productPrice'+'[ownerId='+ownerId+']').text()
	productQty=$('.productQty'+'[ownerId='+ownerId+']').text()
	if(productQty<=0){
		productQty=1;
	}
	productTotalPrice=parseFloat(parseFloat(productPrice)*parseInt(productQty)).toFixed(2);
	$('.productTotalPrice'+'[ownerId='+ownerId+']').text(productTotalPrice);
	orderTotalCheck();
}

function orderTotalCheck(){
	var invTotalPrice = 0;
	$('.productTotalPrice').each(function() {
		invTotalPrice += parseFloat($(this).text());
	});
	$('.invTotalPrice').text(parseFloat(invTotalPrice).toFixed(2));
}
/////

$("body").delegate('.setInvStatus','click',function(event){
	setInvStatus();
});

$("body").delegate('.saveInvData','click',function(event){
	orderTotalCheck();
	updateProducts();
})

$('body').delegate('.removeInvProduct','click',function(){
	ownerId = $(this).attr('ownerId');
	oInvRegNo = $('.oInvRegNo').text();
	data = {
		"productId":ownerId,
		"oInvRegNo":oInvRegNo
	};
	postData(formData=data,url=url_prefix+"/ui/order_inv/",type="DELETE",formId=ownerId);
})

// ajax communications //
function setInvStatus(){
	invoiceData = {
		'invRegNo':$('.invRegNo').text(),
		'oInvRegNo':$('.oInvRegNo').text(),
		'invStatId':$('.orderInvStatus:selected').val()
	}
	postData(formData=invoiceData,url=url_prefix+'/ui/inv_status/',type='POST');
	setTimeout(orderTotalCheck(),1000);
}

function updateProducts(){
	orderData={};
	productData = [];
	$('.productsTable tr').each(function() {
		ownerId = $(this).attr('ownerId');
		productPrice = parseFloat($('.productPrice'+'[ownerId='+ownerId+']').text()).toFixed(2);
		productQty = parseInt($('.productQty'+'[ownerId='+ownerId+']').text());
		totalPrice =  parseFloat($('.productTotalPrice'+'[ownerId='+ownerId+']').text()).toFixed(2);
		productData.push(
			{
				'productId':ownerId,
				'productPrice':productPrice,
				'productQty':productQty,
				'totalPrice':totalPrice
			}
		);

	});
	orderData['oInvRegNo'] = $('.oInvRegNo').text();
	orderData['oInvTotalPrice'] =	parseFloat($('.invTotalPrice').text()).toFixed(2);
	orderData['products'] = productData;
	console.log(orderData);
	postData(formData=orderData,url=url_prefix+'/ui/order_inv/',type='POST');
}