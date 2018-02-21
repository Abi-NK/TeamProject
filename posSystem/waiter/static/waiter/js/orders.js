// populates the page with a list of all orders
function updateOrders(){
  $.get("getorders", function(data){
    alert( "Data Loaded: " + data );
    $("#order-container").html(data);
  });
}

function confirmOrder(button, orderID){
  $.ajax({
    url: "/waiter/confirmorder",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: orderID}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).text("Confirmed");
    }
  });
}

$(document).ready(function(){
  updateOrders();
});
