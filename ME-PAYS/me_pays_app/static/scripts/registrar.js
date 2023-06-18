function sendSelectedValuesRegistrar() {
    var selectedValues = [];
    var shouldExit = false;
    $('.operator').each(function() {
        var selectize = $(this)[0].selectize;
        if (selectize && selectize.getValue() !== "") {
            var value = selectize.getValue();
            var id = $(this).attr('id');
            var qty = $('#' + id + 'qty').val();
            if (qty !== ''){
                selectedValues.push([value, qty]);
            }  else {
                var errorMessage = "Please Select a Quantity";
                var errorContainer = $("#registrar_errorContainer1");
                var displayDuration = 5000; // 5 seconds
                displayErrorMessageWithTimer(
                errorMessage,
                errorContainer,
                displayDuration
                );
                shouldExit = true;
                return false; // Terminate the loop
            }
                
        }
    });
    if (shouldExit) {
        return;
      }
    if (selectedValues.length === 0) {
        // selectedValues is empty
        var errorMessage = "Please Select an Entry";
        var errorContainer = $("#registrar_errorContainer1");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
        );
    } else {
        // selectedValues is not empty
        $.ajax({
        url: "registrar_home/tallyItems",
        method: "GET",
        data: { selectedValues: JSON.stringify(selectedValues) },
        success: function(response) {
            // Handle the success response
            // Parse the serialized data
            var itemData = JSON.parse(response.itemlist);
            // Process the item data as needed
            var priceTotal = 0
            $('#showTally').empty();
            $('#totalAmount').empty();
            $('#FinalTotalAmount').val('');
            itemData.forEach(function(item) {
            printTally(item.id, item.name, item.price, item.quantity);
            // Perform operations with the item data
            // total all prices
            priceTotal += parseInt(item.price);
            });
            document.getElementById("totalAmount").innerText = "Php "+priceTotal.toString();
            var TotalAmount = document.getElementById('FinalTotalAmount');
            TotalAmount.value = parseInt(priceTotal);
            cpay_nextStep(2);
        },
        error: function(xhr, status, error) {
            // Handle the error if the request fails
            console.error("AJAX request failed:", error);
        }
        });
        
    }
}