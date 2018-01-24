// the object of items ordered and quantity
var order = {};
// used locally for displaying order info, should never be returned to the server
var itemNames = {};
var itemPrices = {};
var stringTotal = "total"

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
}

$(document).ready(function() {
  updateTotal();
});
