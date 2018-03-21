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

function getMenuItemDisplay(menuItemID){
  var displayName = itemNames[menuItemID];
  if (order[menuItemID] > 1){
    displayName += ` - (${ order[menuItemID] })`;
  }
  return displayName
}

// adds or updates an entry in the displayed list of items in the order
function updateItemDisplay(){
  $("#order-container").html("");
  $.each(order, function(menuItemID, menuItemQuantity){
    if (menuItemQuantity != 0){
      var entryTemplate = `<div class="card" id="order-item-${ menuItemID }">
        <div class="card-body">
          <div class="row">
            <div class="col-md-9">
              <h4 id="order-item-name-${ menuItemID }">${ getMenuItemDisplay(menuItemID) }</h4>
            </div>
            <div class="col-md-3">
              <h4 id="order-item-price-${ menuItemID }">${ getItemTotalPrice(menuItemID) }</h4>
            </div>
          </div>
        </div>
      </div>`;
      $("#order-container").append(entryTemplate);
    }
  });
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
  updateItemDisplay();
  console.log(menuItemName + " added to order, new total is £" + stringTotal);

  $("#quantity" + menuItemID).html(order[menuItemID])
  $("#containerOrderButton"+menuItemID+" .addButton").hide()
  $("#containerOrderButton"+menuItemID+" .incDecButtons").show()
}

function incOrderItem(menuItemID){
  if (order.hasOwnProperty(menuItemID)) {
    order[menuItemID] += 1;
  } else {
    order[menuItemID] = 1;
  }
  updateTotal();
  updateItemDisplay();
  $("#quantity" + menuItemID).html(order[menuItemID])
}

function decOrderItem(menuItemID){
  if (order.hasOwnProperty(menuItemID)) {
    order[menuItemID] -= 1;
  } else {
    order[menuItemID] = 0;
  }
  if (order[menuItemID] == 0){
    $("#containerOrderButton"+menuItemID+" .addButton").show()
    $("#containerOrderButton"+menuItemID+" .incDecButtons").hide()
  }
  updateTotal();
  updateItemDisplay();
  $("#quantity" + menuItemID).html(order[menuItemID])
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
    $.ajax({
      url: "/core/order/makeorder",
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
    url: "/core/seating/requesthelp",
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
    url: "/core/seating/takeseat",
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
  $.get("/core/orderextra/getorderextra", function(data){
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
    url: "/core/orderextra/cancelorderextraitem",
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

// method called by filtering buttons
$('.filter-btn').on('click', function() {

  if (this.value == "false"){
    $(this).html('<i class="fas fa-times fa-pull-left fa-lg"></i> ' + this.name);
    $(this).removeClass("btn-success").addClass("btn-warning");
    this.value = "true";
  } else {
    $(this).html('<i class="fas fa-check fa-pull-left fa-lg"></i> ' + this.name);
    $(this).removeClass("btn-warning").addClass("btn-success");
    this.value = "false";
  }

  $('.veg-item').show();
  $('.vegan-item').show();
  $('.wheat-item').show();
  $('.nut-item').show();
  $('.meat-item').show();
  $('.milk-item').show();

  // if selected "vegan"
  if($("#vegan").val() == "true"){
    $('.vegan-item').hide();
  }
  // if selected "vegetarian"
  if($("#vegetarian").val() == "true"){
    $('.veg-item').hide();
    $('.vegan-item').hide();
  }
  // if selected "containging meat"
  if($("#meat").val() == "true"){
    $('.meat-item').hide();
  }
  // if selected "wheat-free"
  if($("#wheat-free").val() == "true"){
    $('.wheat-item').hide();
  }
  // if selected "milk-free"
  if($("#milk-free").val() == "true"){
    $('.milk-item').hide();
  }
  // if selected "nut-free"
  if($("#nut-free").val() == "true"){
    $('.nut-item').hide();
  }
});

$(".btn-add").on('click', function(){

});
