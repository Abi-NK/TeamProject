// essentially a wrapper for the HTML template
function makeOrderHTML(){
  return `
  <div class="col-md-12 mb-md-3"><h4>An Order</h4></div>
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
