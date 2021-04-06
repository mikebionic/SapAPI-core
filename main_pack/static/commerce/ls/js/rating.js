
// append .ratingStars list of specified ownerId with <i> icons "fa fa-star-half-o"
function renderStarIconTemplate(iconClassName) {
  return `<i class="`+iconClassName+`"></i>`;
}

function renderRatingStars(ratingValue,ownerId){
	// var ratingValue = 3.6;
	var roundedRate = Math.round(ratingValue*2)/2
	var qty = parseInt(roundedRate);          
	var afterDot = roundedRate - qty
	var sumValues = qty;
	if (afterDot > 0){
	    sumValues = qty+1;
	}
	for (var i=0; i<qty; i++){
		$('.ratingStars'+"[ownerId="+ownerId+"]").append(renderStarIconTemplate("fa fa-star"));
	  // console.log('star');
	}
	if (afterDot>0){
		$('.ratingStars'+"[ownerId="+ownerId+"]").append(renderStarIconTemplate("fa fa-star-half-o"));
	  // console.log('star-half-o');
	}
	for (var i=0; i<(5-sumValues);i++){
	  $('.ratingStars'+"[ownerId="+ownerId+"]").append(renderStarIconTemplate("fa fa-star-o"));
	  // console.log('star-o');
	}	
}

$(document).ready(function(e){
	$('.ratingValue').each(function(){
		var ownerId = $(this).attr('ownerId');
		var ratingValue = $(this).val();
		renderRatingStars(ratingValue,ownerId);
	})
})

