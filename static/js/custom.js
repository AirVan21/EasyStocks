(function ($) {

  "use strict";

    // PROJECT CAROUSEL
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:15,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:true
            },
            600:{
                items:3,
                nav:false
            }
        }
    });

})(jQuery);