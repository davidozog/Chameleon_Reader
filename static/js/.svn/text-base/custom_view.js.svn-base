
$(document).ready(function(){
  var view_state="novice";
  $("div#content .novice").show();
  $("div#content .expert").hide();

  $("a#switch").click(function(event){
    event.preventDefault();
    if (view_state=="novice") {
      // expert view
      view_state = "expert";

      // $(this).text("Show novice view");
      $("div#content .expert").slideDown();
      $("div#content .novice").slideUp();
    } else {
      // novice view
      view_state = "novice";

      // $(this).text("Show expert view");
      $("div#content .novice").slideDown();
      $("div#content .expert").slideUp();
    }
  });
});