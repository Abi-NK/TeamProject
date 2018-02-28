function updateLoop(){
  updateData();
  setTimeout(function(){
     updateLoop();
  }, 5000);
}

function updateData(){
  $.get("getsummary", function(data){
    $("#container-summary").html(data);
  });

  $.get("getorders", function(data){
    $("#container-orders").html(data);
  });
}

$(document).ready(function(){
  updateLoop();
});
