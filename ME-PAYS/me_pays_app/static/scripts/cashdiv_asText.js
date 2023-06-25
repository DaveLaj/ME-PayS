

    
$(document).ready(function () {
    $('input[type="radio"]').click(function () {
      var inputValue = $(this).attr("value");
  
      var nextButton = $("#changebutton");
  
      if (inputValue === "MC-PayS") {
        nextButton.text("Pay RFID");
        nextButton.off("click").on("click", function () {
          pay_nextStep(3); // Custom action for MC-PayS
        });
      } else if (inputValue === "Cash") {
        nextButton.text("Pay Cash");
        nextButton.off("click").on("click", function () {
          // Custom action for Cash
          console.log("Cash selected");
          // Perform the desired action for Cash
        });
      } else {
        nextButton.text("Next");
        nextButton.off("click").on("click", function () {
          // No option selected
          console.log("No option selected");
          // Handle the case when no option is selected
        });
      }
    });
  });
  

  $(document).ready(function () {
    $('#select2').selectize({
        sortField: 'text'
    });
});



function printTally(id, name, price, qty) {
    var newItemAdd = '<tr>' +
                        '<td>'+ id +'</td>'+
                       ' <td>'+ name +'</td>'+
                       ' <td>'+ qty +'</td>'+
                       '<td>'+ price +'</t>'+
                     '</tr>';
    $('#showTally').append(newItemAdd);
}


function printCart(reference_number, paid, datetime) {
  var newItemAdd = '<tr>' +
                      '<td>'+ reference_number +'</td>'+
                     '<td>'+ paid +'</td>'+
                     '<td>'+ datetime +'</td>'+
                     '<td>'+ '<button type="button" class="btn btn-primary"  onclick="cashier_order_info('+ reference_number +')">Proceed</button>' +'</td>'+
                   '</tr>';
  $('#showCart').append(newItemAdd);
}











