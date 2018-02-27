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
}

$(document).ready(function(){
  updateLoop();
});
