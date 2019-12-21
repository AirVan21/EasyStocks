(function ($) {

  "use strict";

    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:15,
        responsiveClass:true,
        responsive:{
            0:{
                items:2,
                nav:false
            },
            970:{
                items:3,
                nav:false
            }
        }
    });

})(jQuery);