$(document).ready(function(){
	viewsCookie = Cookies.get('mostViewed');
	if(viewsCookie == undefined){
    viewsData={};
    Cookies.set('mostViewed',JSON.stringify(viewsData));
	}
	else{
		viewsData=JSON.parse(viewsCookie);
  }
  // ownerId can be provided in view's <scripts> tag
  productId = $('.priceValue').attr('ownerId');
  makeViewed(productId);
});
// price
// name
// category
// image
///// update values on further addition
/////////////// increment quantity
function makeViewed(ownerId){
  // !!! TODO: Rewrite stuff for a ready template
	priceValue = $('.priceValue'+'[ownerId='+ownerId+']').attr('value');
	productImage = $('.productImage'+'[ownerId='+ownerId+']').attr('src');
  productCategory = $('.productCategory'+'[ownerId='+ownerId+']').text();
  productName = $('.productName'+'[ownerId='+ownerId+']').text();
  productUrl = location.href;
  viewedTimes = 1;
  // viewsCookie = Cookies.get('mostViewed');
  // if(viewsCookie == undefined){
	// 	viewsData={};
	// }
  // viewsData = JSON.parse(viewsCookie);
		for (i in viewsData){
      if (viewsData[i]["resId"] == ownerId){
        viewedTimes = viewsData[i]["viewedTimes"] + 1;
        break;
      }
    }
	// saving cookie
	productViewInfo={
    'resId':ownerId,
    'productUrl':productUrl,
    'productName':productName,
    'priceValue':priceValue,
    'productCategory':productCategory,
    'productImage':productImage,
    'viewedTimes':viewedTimes};
	viewsData['product'+ownerId] = productViewInfo;
	Cookies.set('mostViewed',JSON.stringify(viewsData));
}