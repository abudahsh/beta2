//jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".custom-navbar").offset().top > 1) {
        $(".navbar-fixed-top.custom-navbar").removeClass("transparent");
        if ($(".custom-navbar").offset().top == 0 ) {$(".navbar-fixed-top.custom-navbar").addClass("transparent");};
    } else {
        $(".navbar-fixed-top.custom-navbar").addClass("transparent");
    }
});

jQuery(function($) {

    var $nav = $('.fixed-one-page');
    var $win = $(window);
    var winH = $win.height();   // Get the window height.

    $win.on("scroll", function () {
        if ($(this).scrollTop() > winH ) {
            $nav.addClass("navbar-fixed-top");
            $nav.removeClass("absolute-one-page");
        } else {
            $nav.removeClass("navbar-fixed-top");
            $nav.addClass("absolute-one-page");
        }
    }).on("resize", function(){ // If the user resizes the window
       winH = $(this).height(); // you'll need the new height value
    });

});