(function ($) {
 "use strict";

/* mobile menu*/
jQuery('nav#dropdown').meanmenu({
	meanMenuOpen: '<span class="menu-bar"></span>'
});	

/* Nivo slider  */
	$("#gallery-filter").mixitup({
			effects: ['fade','rotateZ'],
			easing: 'snap'
		}); 

/* Nivo slider*/
	$('#ma-inivoslider-banner7').nivoSlider({
		effect: 'random',
		slices: 15,
		boxCols: 8,
		boxRows: 4,
		animSpeed: '600',
		pauseTime: '6000000',
		startSlide: 0,
		directionNav: 1,
		controlNav: 1,
		controlNavThumbs: false,
		pauseOnHover: false,
		manualAdvance: false,
		prevText: '<span class="left"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
		nextText: '<span class="right"><i class="fa fa-angle-right" aria-hidden="true"></i></span>'
	});


/* Type Effect JS */

if ($('.txt-type').length) {
	class TypeWriter {
		constructor(txtElement, words, wait = 3000) {
		  this.txtElement = txtElement;
		  this.words = words;
		  this.txt = "";
		  this.wordIndex = 0;
		  this.wait = parseInt(wait, 10);
		  this.type();
		  this.isDeleting = false;
		}
	  
		type() {
		  // Current index of word
		  const current = this.wordIndex % this.words.length;
		  // Get full text of current word
		  const fullTxt = this.words[current];
	  
		  // Check if deleting
		  if (this.isDeleting) {
			// Remove characters
			this.txt = fullTxt.substring(0, this.txt.length - 1);
		  } else {
			// Add charaters
			this.txt = fullTxt.substring(0, this.txt.length + 1);
		  }
	  
		  // Insert txt into element
		  this.txtElement.innerHTML = `<span class="txt">${this.txt}</span>`;
	  
		  // Initial Type Speed
		  let typeSpeed = 300;
	  
		  if (this.isDeleting) {
			// Increase speed by half when deleting
			typeSpeed /= 2;
		  }
	  
		  // If word is complete
		  if (!this.isDeleting && this.txt === fullTxt) {
			// Make pause at end
			typeSpeed = this.wait;
			// Set delete to true
			this.isDeleting = true;
		  } else if (this.isDeleting && this.txt === "") {
			this.isDeleting = false;
			// Move to next word
			this.wordIndex++;
			// Pause before start typing
			typeSpeed = 500;
		  }
	  
		  setTimeout(() => this.type(), typeSpeed);
		}
	  }
	  
	  // Init On DOM Load
	  document.addEventListener("DOMContentLoaded", init);
	  
	  // Init App
	  function init() {
		const txtElement = document.querySelector(".txt-type");
		const words = JSON.parse(txtElement.getAttribute("data-words"));
		const wait = txtElement.getAttribute("data-wait");
		// Init TypeWriter
		new TypeWriter(txtElement, words, wait);
	  }
}

  
  

/* magnificPopup */
	$('.popup-youtube').magnificPopup({
		disableOn: 700,
		type: 'iframe',
		mainClass: 'mfp-fade',
		removalDelay: 160,
		preloader: false,
		fixedContentPos: false
	});

	$('.image-link').magnificPopup({type:'image'});

/* TOP Menu Stick*/
	$(window).on('scroll',function() {    
	   var scroll = $(window).scrollTop();
	   if (scroll < 200) {
		$("#sticker").removeClass("stick");
	   }else{
		$("#sticker").addClass("stick");
	   }
	}); 

/* syotimer*/
	$('#simple_timer').syotimer({
		year: 2021,
		month: 3,
		day: 17,
		hour: 20,
		minute: 30
	});

 /* scrollUp*/
	$.scrollUp({
	  scrollText: '<i class="fa fa-angle-up" aria-hidden="true"></i>',
	  easingType: 'linear',
	  scrollSpeed: 900,
	  animation: 'fade'
	});

/*slide product carosel*/
	$(".people-say-slide").owlCarousel({
		autoPlay : false,
		items : 1,
		itemsDesktop : [1199,1],
		itemsDesktopSmall : [980,1],
		itemsTablet: [768,1],
		itemsMobile : [479,1],
		slideSpeed : 3000,
		paginationSpeed : 3000,
		rewindSpeed : 3000,
		navigation : true,
		stopOnHover : true,
		pagination : false,
		scrollPerPage:true,
		navigationText : ['<span class="icon-left-open"><i class="fa fa-chevron-left" aria-hidden="true"></i></span>','<span class="icon-right-open"><i class="fa fa-chevron-right" aria-hidden="true"></i></span>'] 
	}); 

/* MailChimp*/
	$('#mc-form').ajaxChimp({
		language: 'en',
		callback: mailChimpResponse,
		// ADD YOUR MAILCHIMP URL BELOW HERE!
		url: 'http://themeshaven.us8.list-manage.com/subscribe/post?u=759ce8a8f4f1037e021ba2922&amp;id=a2452237f8'

	});
	function mailChimpResponse(resp) {
		
		if (resp.result === 'success') {
			$('.mailchimp-success').html('' + resp.msg).fadeIn(900);
			$('.mailchimp-error').fadeOut(400);
			
		} else if(resp.result === 'error') {
			$('.mailchimp-error').html('' + resp.msg).fadeIn(900);
		}  
	}

/* Trigger ColorSwitcher*/
	var colorswitcher = $('.ec-colorswitcher');
	var mainArea = $('.main-area');
	var wrapperBoxed = 'wrapper-boxed';
	var wrapperWide = 'wrapper-wide';
	$('.ec-handle').on('click', function(){
		colorswitcher.trigger('click')
		$(this).toggleClass('btnclose');
		colorswitcher.toggleClass('sidebarmain');
		return false;
	});
	$('.ec-boxed,.pattren-wrap a,.background-wrap a').on('click', function(){
		mainArea.addClass(wrapperBoxed);
		mainArea.removeClass(wrapperWide);
		return false;
	});
	$('.ec-wide').on('click', function(){
		mainArea.addClass(wrapperWide);
		mainArea.removeClass(wrapperBoxed);
		return false;
	});

/* youtube background*/
	$(".youtube-bg").YTPlayer({
			containment:'.youtube-bg',
			autoPlay:true,
			loop:true,
		});

/* Circular Bars - Knob */	
if(typeof($.fn.knob) != 'undefined') {
	$('.knob').each(function () {
	  var $this = $(this),
		  knobVal = $this.attr('data-rel');

	  $this.knob({
		'draw' : function () { 
		  $(this.i).val(this.cv + '%')
		}
	  });
	  
	  $this.appear(function() {
		$({
		  value: 0
		}).animate({
		  value: knobVal
		}, {
		  duration : 2000,
		  easing   : 'swing',
		  step     : function () {
			$this.val(Math.ceil(this.value)).trigger('change');
		  }
		});
	  }, {accX: 0, accY: -150});
	});
	}		
		
})(jQuery);
   