function updateLoop(){
  updateData();
  setTimeout(function(){
     updateLoop();
  }, 5000);
}

function updateWaiters(){
  $.get("/core/waiter/getwaiters", function(data){
    $("#container-waiters").html(data);
  });
}

function updateData(){
  $.get("/core/waiter/getassignments", function(data){
    $("#container-assignments").html(data);
  });
  updateWaiters();
}

$(document).ready(function(){
  updateData();
});

function assignWaiter(button, seating_id, waiter){
  $.ajax({
    url: "/core/seating/assigntoseating",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({username: waiter, seating_id: seating_id}),
    dataType: 'text',
    success: function(result) {
      updateData();
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
      updateData();
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
      updateData();
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
      updateData();
    }
  });
}

function autoAssign(button){
  $(button).html("<i class='fas fa-circle-notch fa-spin'></i>");
  $(button).prop("disabled", true);
  $.ajax({
    url: "/core/waiter/autoassign",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({}),
    dataType: 'text',
    success: function(result) {
      updateData();
      $(button).html("Auto-Assign");
      $(button).prop("disabled", false);
    }
  });
}
