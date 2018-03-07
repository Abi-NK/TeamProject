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

// used to show the customer's order
function showOrder(){
  $('#showOrderModalCenter').modal('show');
}

// used to send the order object to the server
function placeOrder(){
  if (Object.keys(order).length === 0 && Object.keys(orderExtra).length === 0){
    console.log("Not placing order: order is empty.");
  } else {

    var data = {}
    for (var item in order){
      data[item] = order[item];
    }
    for (var item in orderExtra){
      if (item in data){
        data[item] += orderExtra[item]
      } else {
        data[item] = orderExtra[item]
      }
    }

    $.ajax({
      url: "/waiter/makeorder",
      type: 'POST',
      headers: {'X-CSRFToken': csrfToken},
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({order: order}),
      dataType: 'text',
      success: function(result) {
		$('#placeOrderModalCenter').modal('show');
      }
    });
  }
}

function requestHelp(){
  $.ajax({
    url: "/waiter/requesthelp",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({}),
    dataType: 'text',
    success: function(result) {
      $('#callWaiterModalCenter').modal('show');
    }
  });
}

function buttonHelp(button){
  requestHelp();
}

// method called by seating selection buttons to pick a table and tell the server
$('.btn-seating-option').on('click', function(){
  // gets the seating ID from the button's value field
  var seatingID = $(this).attr("value");
  // gets the table's name (label) from the button's name field
  seatingLabel = $(this).attr("name");
  console.log(`Now sitting at ${seatingLabel} (ID ${seatingID})`);

  // sends the selected seating ID to the server so it can be marked as taken, and stored in the user's session
  $('#seating-label').text(seatingLabel);
  $.ajax({
    url: "/customer/takeseat",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({tableID: seatingID}),
    dataType: 'text',
    success: function(result) {
      // if the selection worked, close the seating selection modal
      $('#chooseTableModalCenter').modal('hide');
    }
  });
});

function updateOrderExtra(){
  $.get("getorderextra", function(data){
    $("#container-order-extra").html(data);
  });
}

function updateLoop(){
  updateOrderExtra();
  setTimeout(function(){
     updateLoop();
  }, 5000);
}

function btnOrderExtraRemoveItem(button, order_extra_id, order_item_id){
  $(button).attr("disabled", true);
  console.log("OrderExtra ID: " + order_extra_id);
  console.log("OrderItem ID: " + order_item_id);
  $.ajax({
    url: "/customer/cancelorderextraitem",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({
      order_extra_id: order_extra_id,
      order_item_id: order_item_id,
    }),
    dataType: 'text',
    success: function(result) {
      // if the selection worked, close the seating selection modal
      $('#chooseTableModalCenter').modal('hide');
    }
  });
}

$(document).ready(function() {
  updateTotal();
  if (seatingLabel == ""){
    $('#chooseTableModalCenter').modal('show');
  } else {
    console.log("Already seated at " + seatingLabel);
  }
  updateLoop();
});


// method called by submission button of menu filtering modal
$('.btn-filter').on('click', function() {
  // if selected "vegan"
  if($("#vegan").is(':checked')){
    $('.veg-item').hide();
    $('.meat-item').hide();
  }
  // if selected "vegetarian"
  if($("#vegetarian").is(':checked')){
    $('.meat-item').hide();
  }
  // if selected "wheat-free"
  if($("#wheat-free").is(':checked')){
    $('.wheat-item').hide();
  }
  // if selected "milk-free"
  if($("#milk-free").is(':checked')){
    $('.milk-item').hide();
  }
  // if selected "nut-free"
  if($("#nut-free").is(':checked')){
    $('.nut-item').hide();
  }
  // if selected "meat"
  if($("#meat").is(':checked')){
    $('.veg-item').hide();
    $('.vegan-item').hide();
  }
});

// method called by cancel of filters button
$('.btn-remove').on('click', function() {
  $('.veg-item').show();
  $('.vegan-item').show();
  $('.wheat-item').show();
  $('.nut-item').show();
  $('.meat-item').show();
  $('.milk-item').show();
});
