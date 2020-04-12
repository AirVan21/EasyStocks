(function ($) {
  "use strict";
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:15,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:false
            },
            750:{
              items:2,
               nav:false,
            },
            970:{
                items:3,
                nav:false
            }
        }
    });

})(jQuery);

// Navbaer disabling logic
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos < currentScrollPos) {
    document.getElementById("navigation").style.display = "none";
  } else {
    document.getElementById("navigation").style.display = "initial";
  }
  prevScrollpos = currentScrollPos;
}