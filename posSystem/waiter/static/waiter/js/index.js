function requestHelp(id){
  $.ajax({
    url: "/waiter/cancelhelp",
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({id: id}),
    dataType: 'text',
    success: function(result) {
    }
  });
}
