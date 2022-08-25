jQuery(document).ready(function ($) {
	// cartsAndCheckouts.js
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
			console.log(cartData)
		} else {
			cartData = JSON.parse(cartCookie)
			console.log(cartData)
			for (i in cartData) {
				ownerId = cartData[i]['resId']
				$('.add-to-cart' + '[ownerId=' + ownerId + ']')
					.addClass('added')
					.find('span')
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

	// $('.wishlist-compare a').on('click', function(e){
	// 	e.preventDefault();
	// 	ownerId = $(this).attr('ownerId');

	// 	if($(this).hasClass('added')){
	// 		removeFromWishlist(ownerId);
	// 		$('.wishlist-compare a'+'[ownerId='+ownerId+']').removeClass('added');
	// 	} else{
	// 		addToWishlist(ownerId);
	// 		$('.wishlist-compare a'+'[ownerId='+ownerId+']').addClass('added');
	// 	}
	// });

	$('body').delegate('.addToCart', 'click', function () {
		$(this).hide()
		ownerId = $(this).attr('ownerId')
		addToCart(ownerId)
		$('.add-to-cart' + '[ownerId=' + ownerId + ']')
			.addClass('added')
			.find('span')
			.text(remove_from_cart_text)
	})

	$('body').delegate('.removeFromCart', 'click', function () {
		ownerId = $(this).attr('ownerId')
		removeFromCart(ownerId)
		$('.add-to-cart' + '[ownerId=' + ownerId + ']')
			.removeClass('added')
			.find('span')
			.text(add_to_cart_text)
	})

	$('.add-to-cart').on('click', function (e) {
		e.preventDefault()
		ownerId = $(this).attr('ownerId')

		if ($(this).hasClass('added')) {
			removeFromCart(ownerId)
			$('.add-to-cart' + '[ownerId=' + ownerId + ']')
				.removeClass('added')
				.find('span')
				.text(add_to_cart_text)
		} else {
			addToCart(ownerId)
			$('.add-to-cart' + '[ownerId=' + ownerId + ']')
				.addClass('added')
				.find('span')
				.text(remove_from_cart_text)
		}
	})

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

	$('body').delegate('.add-to-cart', 'click', function () {
		var ownerId = $(this).attr('ownerId')
		var all_this = $('.add-to-cart' + '[ownerId=' + ownerId + ']')
		all_this.hide()
		var qty_obj = all_this.parent().find('.cartItemQty')
		qty_obj.show()
		var qtyvalue = all_this.parent().find('spannput').val()
		if (qtyvalue < 1) {
			all_this.parent().find('spannput').val(1)
		}
		addToCart(ownerId)
	})

	function addToCart(ownerId) {
		if ($('.add-to-cart' + '[ownerId=' + ownerId + ']').hasClass('added')) {
			$('.add-to-cart' + '[ownerId=' + ownerId + ']')
				.removeClass('added')
				.find('span')
				.text('В корзину')
		} else {
			$('.add-to-cart' + '[ownerId=' + ownerId + ']')
				.addClass('added')
				.find('span')
				.text('В корзинe')
		}

		// $('.addToCart'+'[ownerId='+ownerId+']').hide();
		// $('.removeFromCart'+'[ownerId='+ownerId+']').show();
		priceValue = parseFloat(
			$('.priceValue' + '[ownerId=' + ownerId + ']').attr('value'),
		)
		productQty = parseInt($('.productQty' + '[ownerId=' + ownerId + ']').val())
		pending_amount = parseInt(
			$('.productQty' + '[ownerId=' + ownerId + ']').attr('pending_amount'),
		)
		min_amount = parseInt(
			$('.productQty' + '[ownerId=' + ownerId + ']').attr('min_amount'),
		)
		max_amount = parseInt(
			$('.productQty' + '[ownerId=' + ownerId + ']').attr('max_amount'),
		)

		if (productQty > 1) {
		} else {
			productQty = 1
		}

		if (min_amount > 0) {
			if (productQty < min_amount) {
				productQty = min_amount
			}
		}
		if (min_amount > 0) {
			if (productQty > max_amount) {
				productQty = max_amount
			}
		}
		if (
			pending_amount > 0 &&
			productQty > pending_amount &&
			pending_amount < max_amount
		) {
			productQty = pending_amount
		}

		productQty = parseInt(productQty)
		productData = {
			resId: ownerId,
			priceValue: priceValue,
			productQty: productQty,
		}

		cartData = get_local_data_by_name()
		cartData['product' + ownerId] = productData
		// Cookies.set('cart',JSON.stringify(cartData));
		localStorage.setItem('cart', JSON.stringify(cartData))

		if (pending_amount > 0) {
			cartOperations(
				productData,
				url_prefix + '/product/ui_cart/',
				'POST',
				'htmlData',
				'cartItemsList',
			)
		}
		qtyCheckout(ownerId, productQty, min_amount, max_amount, pending_amount)
		totalPriceCheckout(ownerId)
	}

	var addReceiver = $('.add_receiver')
	var addedReceiver = $('.added_receiver')
	var closSvg = $('.close_svg')

	addReceiver.on('click', function (e) {
		e.preventDefault()

		addedReceiver.addClass('open_receiver')
		addReceiver.addClass('none_receiver')
	})

	closSvg.on('click', function (e) {
		e.preventDefault()

		addedReceiver.removeClass('open_receiver')
		addReceiver.removeClass('none_receiver')
	})

	$(document).ready(function () {
		local_cart_data = get_local_data_by_name('cart')
		if (local_cart_data) {
			for (i in local_cart_data) {
				var ownerId = local_cart_data[i]['resId']
				$('.add-to-cart' + '[ownerId=' + ownerId + ']')
					.addClass('added')
					.find('span')
					.text(remove_from_cart_text)
				$('.productQty' + '[ownerId=' + ownerId + ']').val(
					local_cart_data[i]['productQty'],
				)
				totalPriceCheckout(ownerId)
			}
			makeCartRequests(
				local_cart_data,
				`${url_prefix}/product/ui_cart_table/`,
				'PUT',
				'htmlData',
				'cartItemsTable',
			)
		}
	})
	/*--
	Add To wishlist Animation
------------------------*/

	$('.wishlist').on('click', function (e) {
		e.preventDefault()

		if ($(this).hasClass('added_to_wishlist')) {
			$(this).removeClass('added_to_wishlist')
		} else {
			$(this).addClass('added_to_wishlist')
		}
	})

	$('.pagination_link').on('click', function (e) {
		e.preventDefault()

		if ($(this).hasClass('active')) {
			$(this).removeClass('active')
		} else {
			$(this).addClass('active')
		}
	})
	/*--
    Menu Sticky 
-----------------------------------*/
	var windows = $(window)
	var screenSize = windows.width()
	var sticky = $('.workspace-sidebar')

	windows.on('scroll', function () {
		var scroll = windows.scrollTop()
		if (scroll < 100) {
			sticky.removeClass('is-sticky')
		} else {
			sticky.addClass('is-sticky')
		}
	})

	var windows = $(window)
	var screenSize = windows.width()
	var sticky = $('.header-sticky')

	windows.on('scroll', function () {
		var scroll = windows.scrollTop()
		if (scroll < 100) {
			sticky.removeClass('is-sticky')
		} else {
			sticky.addClass('is-sticky')
		}
	})
	var headerCart = $('.header-cart')
	var closeCart = $('.cart-overlay')
	var miniCartWrap = $('.mini-cart-wrap')

	headerCart.on('click', function (e) {
		e.preventDefault()
		$('.cart-overlay').addClass('visible')
		miniCartWrap.addClass('open')
	})
	closeCart.on('click', function (e) {
		e.preventDefault()
		$('.cart-overlay').removeClass('visible')
		miniCartWrap.removeClass('open')
	})

	// sidebar
	var headerSidebar = $('.header-sidebar')
	var closeSidebar = $('.sidebar-overlay')
	var miniSidebarWrap = $('.mini-sidebar-wrap')

	headerSidebar.on('click', function (e) {
		e.preventDefault()
		$('.sidebar-overlay').addClass('visible')
		miniSidebarWrap.addClass('open')
	})
	closeSidebar.on('click', function (e) {
		e.preventDefault()
		$('.sidebar-overlay').removeClass('visible')
		miniSidebarWrap.removeClass('open')
	})

	// var mainAvatar = document.querySelector(".open_filter");
	// var workspace = document.querySelector(".workspace-data");
	// mainAvatar.onclick = function () {
	//   workspace.classList.toggle("open-sidebar");
	// }

	// Category
	var headerCatalog = $('.header-catalog')
	var closeCatalog = $('.catalog-overlay')
	var miniCatalogWrap = $('.mini-catalog-wrap')

	headerCatalog.on('click', function (e) {
		e.preventDefault()
		$('.catalog-overlay').addClass('visible')
		miniCatalogWrap.addClass('open')
	})
	closeCatalog.on('click', function (e) {
		e.preventDefault()
		$('.catalog-overlay').removeClass('visible')
		miniCatalogWrap.removeClass('open')
	})

	// Category
	var headerProfile = $('.header_profile')
	var closeProfile = $('.profile-overlay')
	var miniProfileWrap = $('.menus')

	headerProfile.on('click', function (e) {
		e.preventDefault()
		$('.profile-overlay').addClass('visible')
		miniProfileWrap.addClass('activee')
	})
	closeProfile.on('click', function (e) {
		e.preventDefault()
		$('.profile-overlay').removeClass('visible')
		miniProfileWrap.removeClass('activee')
	})
	/*--
    Hero Slider
--------------------------------------------*/
	var heroSlider = $('.hero-slider')
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
		prevArrow: '<button type="button" class="slick-prev"><i class="icofont icofont-long-arrow-left"></i></button>',
		nextArrow: '<button type="button" class="slick-next"><i class="icofont icofont-long-arrow-right"></i></button>',
	});
	
});
