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
function makeOrderHTML(orderID, items, time, cooking_instructions, confirmed, ready_delivery){
  return `
  <div class="col-md-12 mb-md-3">
    <div class="card">
      <div class="card-body" style="background-color:Tomato;">
        <div class="row">
          <div class="col-md-9">
            <h2 class="card-title">Order #${ orderID }</h2>
            <p class="card-text">Contents:
              ${ items }
            </p>
          </div>
          <div class="col-md-9">
            <p class="card-text">Order made:
                ${ time }
            </p>
          </div>
          <div class="col-md-9">
           <p class="card-text">Cooking:
             ${ cooking_instructions }
           </p>
          </div>
          <div class="col-md-9">
           <p class="card-text">Order status:
             ${ confirmed }
           </p>
         </div>
         <div class="col-md-9">
           <p class="card-text">Order ready:
             ${ ready_delivery }
           </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  `;
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
      var orderHTML = makeOrderHTML(value["pk"], fields["items"], fields["time"], fields["cooking_instructions"], fields["confirmed"], fields["ready_delivery"]);
      $("#order-container").append(orderHTML);
    });

  });
}

function readyOrder(button, orderID){
  $.ajax({
    url: "/waiter/confirmorder",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: orderID}),
    dataType: 'text',
    success: function(result) {
      $(button).attr("disabled", true);
      $(button).text("Ready");
    }
  });
}

$(document).ready(function(){
  updateOrders();
});
