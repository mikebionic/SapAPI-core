
/*--
	Add To Cart Animation
------------------------*/

// $('.add-to-cart').on('click', function(e){
// 	e.preventDefault();

// 	if($(this).hasClass('added')){
// 			$(this).removeClass('added').find('span').text('В корзину');
// 	} else{
// 			$(this).addClass('added').find('span').text('В корзинe');
// 	}
// });	
$(document).ready(function(){
	local_cart_data = get_local_data_by_name('cart');
	if (local_cart_data){
		for (i in local_cart_data){
			var ownerId = local_cart_data[i]["resId"];
			$('.add-to-cart'+'[ownerId='+ownerId+']').addClass('added').find('span').text(remove_from_cart_text);
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
/*--
	Add To wishlist Animation
------------------------*/

$('.wishlist').on('click', function(e){
	e.preventDefault();

	if($(this).hasClass('added_to_wishlist')){
			$(this).removeClass('added_to_wishlist');
	} else{
			$(this).addClass('added_to_wishlist');
	}

});

$('.pagination_link').on('click', function(e){
	e.preventDefault();

	if($(this).hasClass('active')){
		$(this).removeClass('active');
	}else{
		$(this).addClass('active')
	}
})
/*--
    Menu Sticky
-----------------------------------*/
var windows = $(window);
var screenSize = windows.width();
var sticky = $('.header-sticky');

windows.on('scroll', function() {
    var scroll = windows.scrollTop();
    if (scroll < 100) {
        sticky.removeClass('is-sticky');
    }else{
        sticky.addClass('is-sticky');
    }
});
var headerCart = $(".header-cart");
var closeCart = $(".cart-overlay");
var miniCartWrap = $(".mini-cart-wrap");

headerCart.on("click", function (e) {
  e.preventDefault();
  $(".cart-overlay").addClass("visible");
  miniCartWrap.addClass("open");
});
closeCart.on("click", function (e) {
  e.preventDefault();
  $(".cart-overlay").removeClass("visible");
  miniCartWrap.removeClass("open");
});

// sidebar
var headerSidebar = $(".header-sidebar");
var closeSidebar = $(".sidebar-overlay");
var miniSidebarWrap = $(".mini-sidebar-wrap");

headerSidebar.on("click", function (e) {
  e.preventDefault();
  $(".sidebar-overlay").addClass("visible");
  miniSidebarWrap.addClass("open");
});
closeSidebar.on("click", function (e) {
  e.preventDefault();
  $(".sidebar-overlay").removeClass("visible");
  miniSidebarWrap.removeClass("open");
});


// var mainAvatar = document.querySelector(".open_filter");
// var workspace = document.querySelector(".workspace-data");
// mainAvatar.onclick = function () {
//   workspace.classList.toggle("open-sidebar");
// }

// Category
var headerCatalog = $(".header-catalog");
var closeCatalog = $(".catalog-overlay");
var miniCatalogWrap = $(".mini-catalog-wrap");

headerCatalog.on("click", function (e) {
  e.preventDefault();
  $(".catalog-overlay").addClass("visible");
  miniCatalogWrap.addClass("open");
});
closeCatalog.on("click", function (e) {
  e.preventDefault();
  $(".catalog-overlay").removeClass("visible");
  miniCatalogWrap.removeClass("open");
});


/*--
    Hero Slider
--------------------------------------------*/
var heroSlider = $(".hero-slider");
heroSlider.slick({
  arrows: true,
  autoplay: false,
  autoplaySpeed: 5000,
  dots: true,
  pauseOnFocus: false,
  pauseOnHover: false,
  fade: true,
  infinite: true,
  slidesToShow: 1,
  prevArrow:
    '<button type="button" class="slick-prev"><i class="icofont icofont-long-arrow-left"></i></button>',
  nextArrow:
    '<button type="button" class="slick-next"><i class="icofont icofont-long-arrow-right"></i></button>',
});



var addReceiver = $(".add_receiver");
var addedReceiver = $(".added_receiver")
var closSvg = $(".close_svg")

addReceiver.on("click", function (e) {
	e.preventDefault();

	addedReceiver.addClass("open_receiver");
	addReceiver.addClass("none_receiver");
});

closSvg.on("click", function (e) {
  e.preventDefault();
	
  addedReceiver.removeClass("open_receiver");
  addReceiver.removeClass("none_receiver");
});

