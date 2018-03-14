function updateLoop(){
  updateData();
  setTimeout(function(){
     updateLoop();
  }, 5000);
}

function updateData(){
  $.get("getassignments", function(data){
    $("#container-assignments").html(data);
  });

  $.get("getwaiters", function(data){
    $("#container-waiters").html(data);
  });
}

$(document).ready(function(){
  updateLoop();
});
