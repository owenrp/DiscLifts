jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.document.location = $(this).data("url");
    });

// The scrollbar on the conversation_box div in postman/templates/postman/view.html scrolls to the bottom on loading
// Put in a conditional as it was causing an error when loading a page that did not have div.conversation_box
    if ($('div.conversation_box').length > 0){
        $('div.conversation_box').scrollTop($('div.conversation_box')[0].scrollHeight);
    }

});



$(function() {
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "2016:2026",
      // You can put more options here.

    });
  });
