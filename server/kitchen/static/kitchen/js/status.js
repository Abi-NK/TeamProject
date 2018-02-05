// from the django docs: https://docs.djangoproject.com/en/2.0/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrfToken = getCookie('csrftoken');


// essentially a wrapper for the HTML template
function makeOrderHTML(orderID, items, time, cooking_instructions, confirmed, delivered){
  return `
  <div class="col-md-12 mb-md-3">
    <div class="card">
      <div id="body" class="card-body">
        <script>${changeColour(time, this)} </script>
        <div class="row">
          <div class="col-md-9">
            <h2 class="card-title">Order #${ orderID }</h2>
            <p class="card-text">
                <b>Items:</b> <br> ${ items }
            </p>
            <p>
                <b>Time:</b> &nbsp; ${ parseTime(time, 'H') +":" +  parseTime(time, 'M') + ":"+ parseTime(time, 'S') }
            </p>
            <p>
                <b>Cooking instructions:</b> &nbsp; ${ cooking_instructions }
            </p>
            <p>
                <b>Order Confirmed:</b> &nbsp; ${ easyRead(confirmed) }
            </p>
            <p>
                <b>Order delivered status:</b> &nbsp; ${ easyRead(delivered) }
            </p>
          </div>
          <div class="col-md-3 text-center">
            <button type="button" class="btn btn-primary btn-lg"
            onclick="setReadyDelivery(this, ${ orderID })" ${ confirmed ? "disabled" : "" }>
            ${ confirmed ? "readied" : "ready" }</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  `;
}

// makes boolean vars easyer to read
// returns eather yes or no strings depending on bool
function easyRead(bool){
    if (bool){
        return "yes";
    } else {
        return "no";
    }
}

// this function returns the current time --> needs fixing
function timeNow(){
    var d = new Date();
    d = d.getTime();
    return d;
}

// time parser that takes argument of frame
// returns houres, mins or secs depengin on frame
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

// returns date
function parseDate(time){
    var timeString = time;
    var DateOnly = timeString.slice(0, 9);
    return DateOnly;
}

//changes color depenign on the age of the order
function changeColour(time, id) {

    var d = new Date();
    d = d.getTime();

    var orderTimeM = parseTime(time, 'M');

    if((orderTimeM - 10) > d){
        document.getElementsByClassName("card-body").style.backgroundColor = "RED";
    }else{
        //document.getElementById("body").style.backgroundColor = "GREEN";
        //document.getElementsByClassName("card-body").style.backgroundColor = "RED";
        document.getElementById(id).style.backgroundColor = "GREEN";
    }
}

// populates the page with a list of all orders
function updateOrders(){
  $.getJSON("getorders", function(data){
    var ordersJSON = JSON.parse(data)
    console.log(data);
    console.log(ordersJSON);

    // for each order in ordersJSON
    $.each(ordersJSON, function(key, value){
      var fields = value["fields"];
      var orderHTML = makeOrderHTML(value["pk"], fields["items"], fields["time"], fields["cooking_instructions"], fields["ready_delivery"], fields["delivered"]);
      $("#order-container").append(orderHTML);
    });

  });
}

function setReadyDelivery(button, orderID){ //add check for confirmed first
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
