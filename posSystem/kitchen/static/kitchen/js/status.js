// Refreshes the  page every 30 seconds
// this is to keep the orders up to date
// and to track progress using the colour system
function updateLoop(){
  updateOrders();
  setTimeout(function(){
     updateLoop();
  }, 5000);
}


// populates the page with a list of all orders
function updateOrders(){
  $.get("/core/order/html/kitchen_cards", function(data){
    $("#order-container").html(data);
    $(".not-late .card-header").css("background-color", "LIGHTGREEN");
    $(".nearly-late .card-header").css("background-color", "#FEDB00");
    $(".late .card-header").css("background-color", "#F15454");
  });
}

// Makes the order ready for delivery by setting the ready_delivery field
// in the Order db to True.
function setReadyDelivery(button, orderID){
  $.ajax({
    url: "/core/order/readyDelivery",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: orderID}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).removeClass("btn-primary").addClass("btn-success")
      $(button).text("Readied");
    }
  });
}

$(document).ready(function(){
  updateLoop();
});
