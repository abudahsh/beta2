$('link[href="css/color.css"]').attr('href','css/colors/5.css');


$(function(){
      // if text box value is not null, then darken reset icon
      $(".slinput input").keyup(function(){
        var val = $(this).val();   
        if(val.length > 0) {
           $(this).parent().find(".left-icon").addClass('hastext');
           $(this).parent().find(".left-icon").removeClass('hasnotext');
        } else {
          $(this).parent().find(".left-icon").addClass('hasnotext');
          $(this).parent().find(".left-icon").removeClass('hastext');
        }
      });
      
      // if user click on reset icon, clear text field
      $(".slinput .left-icon").click(function(){
        $(this).parent().find("input").val('');
        $(this).addClass('hasnotext');
        $(this).removeClass('hastext');
      });
});







 (function($){
  $(document).ready(function(){
    $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
      event.preventDefault(); 
      event.stopPropagation(); 
      $(this).parent().siblings().removeClass('open');
      $(this).parent().toggleClass('open');
    });
  });
})(jQuery);

//var ma = ["sub1","sub2","sub4","sub5","sub6","sub7"];
var ma = ["sub1","sub2"];
function dropmenu(x) {

  for (var i = 0, len = ma.length; i < len; i++) {
    if (ma[i] != x) {
      document.getElementById(ma[i]).style.display = "none";
    }
  }
  
  
  if (document.getElementById(x).style.display == "block") {
    document.getElementById(x).style.display = "none";
  } else {

    document.getElementById(x).style.display = "block";
  }
}

$(window).click(function() {
  for (var i = 0, len = ma.length; i < len; i++) {
    document.getElementById(ma[i]).style.display = "none";
  }
});





var status = 0;
$( ".toggle-verticalmenu" ).click(function() {
    $(".Vertical-menu").toggle(100);
    $("#menuoverlay").toggle(100);
    $('body').toggleClass("noscroll");
});

$("#menuoverlay").click(function() {
    $(".Vertical-menu").hide(100);
    $("#menuoverlay").hide(100);
    $('body').removeClass("noscroll");
});

methodToFixLayout();

$(window).on("resize", methodToFixLayout);

function methodToFixLayout( e ) {
    var wininnerWidth = window.innerWidth;
    var winheight = $(window).height();
    var headerheight = $('#menu-header').height();

    $("#menu-content").css("height",winheight-headerheight);

    $(".Vertical-menu").hide(100);
    $("#menuoverlay").hide(100);
    
    $('body').removeClass("noscroll");

    //if (wininnerWidth < 768) {
    //  $(".slinput input").css("width",wininnerWidth-120);    
    //} else { $(".slinput input").css("width",""); }
}





$(window).load(function(){
  $("#categories-dropdown li a").click(function(){

    $(".categories-dropdown-btn").addClass("collapsed");
    
      $(".categories-dropdown-btn:first-child").html($(this).text() + '<i class="fa fa-chevron-up"></i>');
  });
});
