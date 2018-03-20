function requestHelp(id){
  $.ajax({
    url: "/core/seating/cancelhelp",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: id}),
    dataType: 'text',
    success: function(result) {
    }
  });
}

function updateLoop(){
  updateOrders();
  setTimeout(function(){
     updateLoop();
  }, 5000);
}

function updateOrders(){
  $.get("/core/seating/html/waiters_seating_list", function(data){
    $("#container-tables").html(data);
  });

  $.get("/core/seating/html/assistance_alerts", function(data){
    $("#container-alerts").html(data);
  });

  $.get("/core/order/html/confirm_cards", function(data){
    $("#container-confirm").html(data);
  });

  $.get("/core/order/html/delivery_cards", function(data){
    $("#container-delivery").html(data);
  });

  $.get("/core/order/html/unpaid_cards", function(data){
    $("#container-unpaid").html(data);
  });
}

function confirmOrder(button, orderID){
  $.ajax({
    url: "/core/order/confirmorder",
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

function delayOrder(button, orderID){
  $.ajax({
    url: "/core/order/delayorder",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: orderID}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).removeClass("btn-primary").addClass("btn-success")
      $(button).text("Delayed");
    }
  });
}

function confirmPayment(button, paymentID){
  $.ajax({
    url: "/core/payment/confirmPayment",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: paymentID}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).removeClass("btn-primary").addClass("btn-success")
      $(button).text("Confirmed");
    }
  });
}

function cancelOrder(button, orderID){
  $.ajax({
    url: "/core/order/cancelorder",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: orderID}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).text("Cancelled");
    }
  });
}

function openModalOrderExtra(){
  $.get("/core/seating/html/occupied_seating_dropdown", function(data){
    $("#inputSeating").html(data);
    $('#modalOrderExtra').modal('show');
  });
}

$("#inputQuantityDec").click(function(){
  document.getElementById("inputQuantity").stepDown();
});

$("#inputQuantityInc").click(function(){
  document.getElementById("inputQuantity").stepUp();
});

$("#btnPlaceOrderExtra").click(function(){
  var seating_id = $("#inputSeating").val();
  var menu_item_id = $("#inputMenuItem").val();
  var quantity = $("#inputQuantity").val();
  console.log("Seating ID: " + seating_id);
  console.log("Menu item ID: " + menu_item_id);
  console.log("Quantity: " + quantity);

  if (seating_id == -1){
    console.log("Seating was not selected.");
  } else if (menu_item_id == -1){
    console.log("Menu item was not selected.");
  } else {
    var data = {
      seating_id: seating_id,
      menu_item_id: menu_item_id,
      quantity: quantity,
    }

    $.ajax({
      url: "/core/orderextra/placeorderextra",
      type: 'POST',
      headers: {'X-CSRFToken': csrfToken},
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify(data),
      dataType: 'text',
      success: function(result) {
        $('#modalOrderExtra').modal('hide');
      }
    });
  }
});

function openModalSeating(){
  $.get("/core/seating/html/assignment_list", function(data){
    $("#container-seating").html(data);
    $('#modalSeating').modal('show');
  });
}

function assignWaiter(button, seating_id, waiter){
  $.ajax({
    url: "/core/seating/assigntoseating",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({username: waiter, seating_id: seating_id}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).text("assigned");
      $.get("/core/seating/html/assignment_list", function(data){
        $("#container-seating").html(data);
      });
    }
  });
}

function unassignWaiter(button, seating_id, waiter){
  $.ajax({
    url: "/core/seating/unassignfromseating",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({username: waiter, seating_id: seating_id}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).text("unassigned");
      $.get("/core/seating/html/assignment_list", function(data){
        $("#container-seating").html(data);
      });
    }
  });
}

function waiterOnDuty(button, username){
  $(button).html("<i class='fas fa-circle-notch fa-spin'></i>");
  $(button).prop("disabled", true);
  $.ajax({
    url: "/core/waiter/waiteronduty",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({name: username}),
    dataType: 'text',
    success: function(result) {
      updateOrders();
    }
  });
}

function waiterOffDuty(button, username){
  $(button).html("<i class='fas fa-circle-notch fa-spin'></i>");
  $(button).prop("disabled", true);
  $.ajax({
    url: "/core/waiter/waiteroffduty",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({name: username}),
    dataType: 'text',
    success: function(result) {
      updateOrders();
    }
  });
}

$("#removeButton").click(function(){
  var itemToRemoveID = $("#removeMenuItem").val();
  var removalData = {
      itemToRemoveID: itemToRemoveID
  }
    $.ajax({
      url: "/core/menu/removemenuitem",
      type: 'POST',
      headers: {'X-CSRFToken': csrfToken},
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify(removalData),
      dataType: 'text',
      success: function(result) {
        $('#removal').modal('hide');
      }
    });
});

$(document).ready(function(){
  updateLoop();
});
