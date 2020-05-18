(function ($) {
  "use strict";
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:20,
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

function dynamicColors() {
  var r = Math.floor(Math.random() * 255);
  var g = Math.floor(Math.random() * 255);
  var b = Math.floor(Math.random() * 255);
  return "rgba(" + r + "," + g + "," + b + ", 0.5)";
}

function poolColors(array_size) {
  // set default colors
  var pool = [
    "rgba(7,83,118, 0.5)",
    "rgba(104,87,121, 0.5)",
    "rgba(138,235,165, 0.5)",
    "rgba(200,166,140, 0.5)",
    "rgba(164,238,254, 0.5)",
  ];
  for(i = pool.length; i < array_size; i++) {
      pool.push(dynamicColors());
  }
  return pool.slice(0, array_size)
}