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

// the object of items ordered and quantity
var order = {};
// used locally for displaying order info, should never be returned to the server
var itemNames = {};
var itemPrices = {};
var stringTotal = "total"

var tableNumber = "0";

// returns the sum of all items in the order times their quantity
function calculateTotal(){
  var total = 0;
  for (const [item, quantity] of Object.entries(order)){
    total += (itemPrices[item] * quantity);
  }
  return total;
}

// calculates the total, stores the 2dp string version, updates on screen total
function updateTotal(){
  var total = calculateTotal()
  stringTotal = Number.parseFloat(total).toFixed(2);
  $("#total-price").text("£" + stringTotal);
}

function getItemTotalPrice(menuItemID){
  if (order.hasOwnProperty(menuItemID) && itemPrices.hasOwnProperty(menuItemID)){
    var price = order[menuItemID] * itemPrices[menuItemID];
    return "£" + Number.parseFloat(price).toFixed(2);
  } else {
    return "£0.00";
  }
}

// adds or updates an entry in the displayed list of items in the order
function addOrderItemToDisplay(menuItemID){
  if ($("#order-item-" + menuItemID).length == 0) {
    // item does not exist in order list yet, so add it
    var entryTemplate = `<div class="card" id="order-item-${ menuItemID }">
      <div class="card-body">
        <div class="row">
          <div class="col-md-9">
            <h4 id="order-item-name-${ menuItemID }">${ itemNames[menuItemID] }</h4>
          </div>
          <div class="col-md-3">
            <h4 id="order-item-price-${ menuItemID }">${ getItemTotalPrice(menuItemID) }</h4>
          </div>
        </div>
      </div>
    </div>`;
    $("#order-container").append(entryTemplate);
  } else {
    // item is already in list, so update it's entry
    // updates the item name to have " - (n)" appended
    var itemText = itemNames[menuItemID];
    if (order[menuItemID] > 1){
      itemText += ` - (${ order[menuItemID] })`;
    }
    $("#order-item-name-" + menuItemID).text(itemText);

    // updates total
    $("#order-item-price-" + menuItemID).text(getItemTotalPrice(menuItemID));
  }
}

// called by buttons on menu items, ads them to the order object
function addToOrder(menuItemID, menuItemName, menuItemPrice) {
  // increment the counter for that menu item, or create it
  if (order.hasOwnProperty(menuItemID)) {
    order[menuItemID] += 1;
  } else {
    order[menuItemID] = 1;
  }

  // update the name and price of the menu item for order displaying
  itemNames[menuItemID] = menuItemName;
  itemPrices[menuItemID] = menuItemPrice;

  updateTotal();
  console.log(menuItemName + " added to order, new total is £" + stringTotal);
  addOrderItemToDisplay(menuItemID);
}

// used to send the order object to the server
function placeOrder(){
  if (Object.keys(order).length === 0){
    console.log("Not placing order: order is empty.");
  } else {
    $.ajax({
      url: "/waiter/makeorder",
      type: 'POST',
      headers: {'X-CSRFToken': csrfToken},
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify(order),
      dataType: 'text',
      success: function(result) {
        alert("Order sent!");
      }
    });
  }
}

function askTableNumber(){
  // could store the table number server-side with sessions in future
  input = prompt("Which table number are you sitting at?");
  while(isNaN(input) || input == null){
    input = prompt("Sorry, that didn't look like a number, where are you sitting?");
  }
  tableNumber = input;
}

function requestHelp(){
  $.ajax({
    url: "/waiter/requesthelp",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({tableNumber: tableNumber}),
    dataType: 'text',
    success: function(result) {
      alert("Someone will be with you shortly");
    }
  });
}

$(document).ready(function() {
  updateTotal();
  askTableNumber();
  console.log(tableNumber);
  requestHelp();
});
