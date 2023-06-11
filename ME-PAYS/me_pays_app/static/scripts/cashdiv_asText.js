// <!-- Add Document CashDiv Query -->

var selectCount = 1;

$("#addFile").click(function () {
    $.ajax({
        url: "cashdiv_home/fetchServices",
        method: "GET",
        success: function (response) {
            // Process the product data and generate the dynamic HTML content
            var optionsHtml = '';
            var selectClass = "select2" + selectCount;
            response.services.forEach(function (product) {
                optionsHtml += '<option value="' + product.id + '">' + product.menu_name + '</option>';
            });

            // Replace the placeholder in newRowAdd with the dynamic HTML content
            var newRowAdd = '<div id="row" class="mb-3 d-flex">' +
                '<label class="col-sm-2 col-form-label"></label>' +
                '<select id="' + selectClass + '" style="width:200px;" class="operator ' + selectClass + '">' +
                ' <option value="">Select an item</option>' +
                optionsHtml +
                '</select>' +
                '<button class="btn btn-danger" id="DeleteRow" type="button"> Cancel</button>' +
                '</div>';

            // Append the updated newRowAdd to #newinput
            $('#newinput').append(newRowAdd);

            // Initialize the selectize plugin for the newly added select element
            $('#' + selectClass).selectize({
                sortField: 'text'
            });

            selectCount++;
        },
        error: function (xhr, status, error) {
            // Handle errors if the request fails
            var errorMessage = "Fetch Error!";
            var errorContainer = $("#statusContainer");
            var displayDuration = 5000; // 5 seconds
            displayErrorMessageWithTimer(
                errorMessage,
                errorContainer,
                displayDuration
            );
        }
    });
});



$(document).ready(function () {
    $('.select2').selectize({
        sortField: 'text'
    });
});
    
$("body").on("click", "#DeleteRow", function () {
    $(this).parents("#row").remove();
})
    

    
$(document).ready(function () {
    $('input[type="radio"]').click(function () {
        var inputValue = $(this).attr("value");
        var targetBox = $("." + inputValue);
       
        var nextButton = $("#changebutton");
        nextButton.off("click"); // Remove previous click event handler

        if (inputValue === "MC-PayS") {
        nextButton.on("click", function () {
            // Custom action for MC-PayS
            console.log("MC-PayS selected");
            // Perform the desired action for MC-PayS
        });
        } else if (inputValue === "Cash") {
        nextButton.on("click", function () {
            // Custom action for Cash
            console.log("Cash selected");
            // Perform the desired action for Cash
        });
        } else {
        nextButton.on("click", function () {
            // No option selected
            console.log("No option selected");
            // Handle the case when no option is selected
        });
        }
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
