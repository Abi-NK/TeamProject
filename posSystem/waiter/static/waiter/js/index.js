function requestHelp(id){
  $.ajax({
    url: "/waiter/cancelhelp",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: id}),
    dataType: 'text',
    success: function(result) {
    }
  });
}

function updateOrders(){
  $.get("getalerts", function(data){
    $("#container-alerts").html(data);
  });

  $.get("getordersconfirm", function(data){
    $("#container-confirm").html(data);
  });

  $.get("getordersdelivery", function(data){
    $("#container-delivery").html(data);
  });

  $.get("getordersunpaid", function(data){
    $("#container-unpaid").html(data);
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
      $(button).removeClass("btn-primary").addClass("btn-success")
      $(button).text("Confirmed");
    }
  });
}

$(document).ready(function(){
  updateOrders();
});
