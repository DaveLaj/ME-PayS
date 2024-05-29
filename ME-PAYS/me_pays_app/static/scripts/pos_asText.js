var selectCount = 2;

$("#addProduct").click(function () {
    $.ajax({
        url: "pos_home/fetchProducts",
        method: "GET",
        success: function (response) {
            // Process the product data and generate the dynamic HTML content
            var optionsHtml = '';
            var selectClass = "posselect" + selectCount;
            response.services.forEach(function (product) {
                optionsHtml += '<option value="' + product.id + '">' + product.menu_name + '</option>';
            });

            // Replace the placeholder in newRowAdd with the dynamic HTML content
            var newRowAdd = 
                '<div id="row" class="row g-3" >' +
                    ' <div class="col-md-8">' +
                        '<select id="' + selectClass + '"  class="operator">' +
                            ' <option value="">Select document</option>' +
                            optionsHtml +
                        '</select>' +
                    '</div>' +
                    '<div class="col-md-2">' +
                        '<input type="text" class=" form-control " id="'+selectClass+'qty" >' +
                    '</div>' +
                    '<div class="col-md-2 d-grid mx-auto pb-2">' +
                        '<button class="btn btn-danger" id="DeleteRow" type="button" > Cancel</button>' +
                    '</div>'+
                '</div>';

            // Append the updated newRowAdd to #newinput
            $('#newproduct').append(newRowAdd);

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
    $('#posselect1').selectize({
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
















$("#addProdus").click(function () {
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