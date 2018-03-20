function updateLoop(){
  updateData();
  setTimeout(function(){
     updateLoop();
  }, 5000);
}

function updateData(){
  $.get("/core/order/html/summary_list", function(data){
    $("#container-summary").html(data);
  });

  $.get("/core/order/html/active_list", function(data){
    $("#container-orders").html(data);
  });

  $.get("/core/seating/html/manager_list", function(data){
    $("#container-tables").html(data);
  });

  $.get("/core/menu/html/stock_list", function(data){
    $("#container-stock").html(data);
  });
}

$(document).ready(function(){
  updateLoop();
});
