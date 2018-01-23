// the object of items ordered and quantity
var order = {};
// used locally for displaying order info, should never be returned to the server
var itemNames = {};
var itemPrices = {};

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

  console.log(order);
  console.log(itemNames);
  console.log(itemPrices);
  calculateTotal();
}

$(document).ready(function() {
  $("#total-price").text("£0.00");
});
