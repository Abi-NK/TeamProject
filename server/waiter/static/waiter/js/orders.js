// essentially a wrapper for the HTML template
function makeOrderHTML(){
  return `
  <div class="col-md-12 mb-md-3">
    <div class="card">
      <div class="card-body">
        <div class="row">
          <div class="col-md-9">
            <h2 class="card-title">Order Number</h2>
            <p class="card-text">
              Items which have been ordered.
            </p>
          </div>
          <div class="col-md-3">

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
      var orderHTML = makeOrderHTML();
      $("#order-container").append(orderHTML);
    });

  });
}

$(document).ready(function(){
  updateOrders();
});
