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
  //  viewsData={};
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

$(document).ready(function(){
	viewsCookie = Cookies.get('mostViewed');
	if(viewsCookie == undefined){
    viewsData={};
    Cookies.set('mostViewed',JSON.stringify(viewsData));
	}
	else{
    viewsData=JSON.parse(viewsCookie);
  }
  mostViewedBlock = $('.mostViewedList');
  
  var items = Object.keys(viewsData).map(function(key) {
    return [key, viewsData[key]];
  });

  items.sort(function(first, second) {
    return second[1]['viewedTimes'] - first[1]['viewedTimes'];
  });

  sortedViewsData = items.slice(0, 5);

  // console.log(sortedViewsData)
  // // example output
  // [
  //   [
  //     "product6",
  //     {
  //       "resId":"6",
  //       "productUrl":"http://127.0.0.1:5000/commerce/product/6",
  //       "productName":"ÝÜPEK SAPAK NOOR 502",
  //       "priceValue":"9.5",
  //       "productCategory":"Kategoriýa: NOOR YUPEK SAPAKLAR",
  //       "productImage":"/ls/api/get-image/image/M/a8b7cc6780902ecd75f06e9a11a8.jpg",
  //       "viewedTimes":4
  //     }
  //   ]
  // ]

  for (i in sortedViewsData){
    resId = sortedViewsData[i][1]["resId"];
    productUrl = sortedViewsData[i][1]["productUrl"];
    productName = sortedViewsData[i][1]["productName"];
    priceValue = sortedViewsData[i][1]["priceValue"];
    productCategory = sortedViewsData[i][1]["productCategory"];
    productImage = sortedViewsData[i][1]["productImage"];
    viewedTimes = sortedViewsData[i][1]["viewedTimes"];;
    
    viewsHtmlTemplate = renderViewsTemplate(resId,productUrl,productName,productCategory,productImage,priceValue);
    mostViewedBlock.append(viewsHtmlTemplate);
  }
});


function renderViewsTemplate(resId,productUrl,productName,productCategory,productImage,priceValue) {
  return `<li class="pr-item">
  <div class="contain-product style-widget">
    <div class="product-thumb">
      <a href="`+ productUrl +`" class="link-to-product" tabindex="0">
        <img loading="lazy" src="`+ productImage +`" alt="dd" width="270" height="270" class="product-thumnail">
      </a>
    </div>
    <div class="info">
      <b class="categories">`+ productCategory +`</b>
      <h4 class="product-title"><a href="`+ productUrl +`" class="pr-name" tabindex="0">`+ productName +`</a></h4>
      <div class="price">
        <ins><span class="price-amount"><span class="currencySymbol">TMT </span>`+ priceValue +`</span></ins>
      </div>
    </div>
  </div>
</li>`;
}