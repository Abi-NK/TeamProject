function updateLoop(){

  $.get("/core/order/html/customer_cards", function(data){
    $("#container-customer-cards").html(data);
  });

  setTimeout(function(){
     updateLoop();
  }, 5000);
}

$(document).ready(function() {
  updateLoop();
});
