

function printTallyRegistrar(id, name, price, qty) {
    var newItemAdd = '<tr>' +
                        '<td>'+ id +'</td>'+
                       ' <td>'+ name +'</td>'+
                       ' <td>'+ qty +'</td>'+
                       '<td>'+ price +'</t>'+
                     '</tr>';
    $('#showTally').append(newItemAdd);
}







var selectCount = 2;

$("#addService").click(function () {
    $.ajax({
        url: "registrar_home/fetchServices",
        method: "GET",
        success: function (response) {
            // Process the product data and generate the dynamic HTML content
            var optionsHtml = '';
            var selectClass = "select" + selectCount;
            response.services.forEach(function (product) {
                optionsHtml += '<option value="' + product.id + '">' + product.name + '</option>';
            });

            // Replace the placeholder in newRowAdd with the dynamic HTML content
            var newRowAdd = 
                '<div id="row" class="row g-3 fs-5" >' +
                    ' <div class="col-md-8">' +
                        '<select id="' + selectClass + '"  class="operator">' +
                            ' <option value="">Select document</option>' +
                            optionsHtml +
                        '</select>' +
                    '</div>' +
                    '<div class="col-md-2">' +
                        '<input type="text" class=" form-control " id="'+selectClass+'qty"  style="height: 45px;">' +
                    '</div>' +
                    '<div class="col-md-2 d-grid mx-auto pb-3">' +
                        '<button class="btn btn-danger" id="DeleteRow" type="button"  style="height: 45px;"> Cancel</button>' +
                    '</div>'+
                '</div>';

            // Append the updated newRowAdd to #newinput
            $('#newinput').append(newRowAdd);
            // '<button class="btn btn-danger" id="DeleteRow" type="button"> Cancel</button>' +
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
    $('#select1').selectize({
        sortField: 'text'
    });
});
    
$("body").on("click", "#DeleteRow", function () {
    $(this).parents("#row").remove();
})
    