// // essentially a wrapper for the HTML template
// function showOrders(orderID, items, time, cooking_instructions, confirmed, ready_delivery, delivered){
//   return `
//   <div class="col-md-12 mb-md-3">
//     <div class="card">
//       <div id="body" class="card-body" style=${changeColour(time)}>
//         <div class="row">
//           <div class="col-md-9">
//             <h2 class="card-title">Order #${ orderID }</h2>
//             <p class="card-text">
//                 <b>Items:</b> <br> ${ items }
//             </p>
//             <p>
//                 <b>Order time:</b> &nbsp; ${ parseTime(time, 'H') +":" +  parseTime(time, 'M') + ":"+ parseTime(time, 'S') }
//             </p>
//             <p>
//                 <b>Cooking instructions:</b> &nbsp; ${ cooking_instructions }
//             </p>
//             <p>
//                 <b>Order Confirmed:</b> &nbsp; ${ easyRead(confirmed) }
//             </p>
//             <p>
//                 <b>Order delivered:</b> &nbsp; ${ easyRead(delivered) }
//             </p>
//           </div>
//           <div class="col-md-3 text-center">
//             <button type="button" class="btn btn-primary btn-lg"
//             onclick="setReadyDelivery(this, ${ orderID })" ${ ready_delivery ? "disabled" : "" }>
//             ${ ready_delivery ? "readied" : "ready" }</button>
//           </div>
//         </div>
//       </div>
//     </div>
//   </div>
//   `;
// }

// makes boolean vars easier to read
// returns either yes or no strings depending on bool
function easyRead(bool){
    if (bool){
        return "yes";
    } else {
        return "no";
    }
}

// this function returns the current time
function timeNow(){
    var d = new Date();
    d = d.getTime();
    return d;
}

// time parser that takes argument of frame
// returns hours, minutes or secs depending on frame
function parseTime(time, frame){
    var timeString = time;

    if (frame == 'H'){
        var timeOnly = timeString.slice(11, 13);
    } else if (frame == 'M'){
        var timeOnly = timeString.slice(14, 16);
    } else if (frame == 'S'){
        var timeOnly = timeString.slice(17, 19);
    }
    return timeOnly;
}

// returns date from the time field that is passed in
// needs to be formatted using the Django datetimefield format
function parseDate(time){
    var timeString = time;
    var DateOnly = timeString.slice(0, 9);
    return DateOnly;
}

// changes color depending on the age of the order
// note: parseTime function will not work to parse for the function bellow,
// instead a local parser is used.

// PLEASE do not read the function bellow. I am sorry. Please don't judge me.
function changeColour(time) {

    var date = new Date();
    var currentTimeMinutes = date.getMinutes();
    if ((currentTimeMinutes.toString().length) == 1){
        currentTimeMinutes = "0" + String(currentTimeMinutes); // 0 is used to match the format of datetimefield
    }
    var currentTimeHour = date.getHours();
    if ((currentTimeHour.toString().length) == 1){
        currentTimeHour = "0" + String(currentTimeHour);
    }

    var orderTimeMinutes = time.slice(14, 16);
    var orderTimeHour = time.slice(11, 13);

    // handle overflow
    if (parseInt(orderTimeMinutes) >= 59){
        orderTimeMinutes = "00";
    }

    // add the 10 and 3 as this is when the order is due. Possible overflow at 60
    if ((parseInt(orderTimeHour)) < (parseInt(currentTimeHour))){
        return "background-color:#F15454;"
    }
    else if((parseInt(orderTimeMinutes)+10) <= (parseInt(currentTimeMinutes))){
        return "background-color:#F15454;"
    }else if((parseInt(orderTimeMinutes)+7) <= (parseInt(currentTimeMinutes)) && (parseInt(orderTimeMinutes)+9) >= (parseInt(currentTimeMinutes)) ){
        return "background-color:#FEDB00;"
    }else {
        return "background-color:LIGHTGREEN;"
    }
}// ^I am sorry you had to look at this.

// Refreshes the  page every 30 seconds
// this is to keep the orders up to date
// and to track progress using the colour system
setTimeout(function(){
   window.location.reload(1);
}, 30000);

// populates the page with a list of all orders
function updateOrders(){
  $.get("getorders", function(data){
    $("#order-container").html(data);
    $(".not-late").css("background-color", "LIGHTGREEN");
    $(".almost-late").css("background-color", "#FEDB00");
    $(".late").css("background-color", "#F15454");
    // var ordersJSON = JSON.parse(data)
    // console.log(data);
    // console.log(ordersJSON);
    //
    // // for each order in ordersJSON
    // $.each(ordersJSON, function(key, value){
    //   var fields = value["fields"];
    //   var orderHTML = showOrders(value["pk"], fields["items"], fields["time"], fields["cooking_instructions"],
    //    fields["confirmed"], fields["ready_delivery"], fields["delivered"]);
    //   $("#order-container").append(orderHTML);
    // });

  });
}

// Makes the order ready for delivery by setting the ready_delivery field
// in the Order db to True.
function setReadyDelivery(button, orderID){
  $.ajax({
    url: "/kitchen/readyDelivery",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: orderID}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).text("readied");
    }
  });
}

$(document).ready(function(){
  updateOrders();
});
