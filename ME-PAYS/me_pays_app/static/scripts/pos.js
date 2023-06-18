
var cpay_currentStep = 1;
function cpay_showStep(step) {
    $(".modal").modal("hide");
    $("#cpaystep" + step + "Modal").modal("show");
}


function cpay_nextStep(step) {
    cpay_currentStep = step;
    cpay_showStep(cpay_currentStep);
    if (step == 3) {
        $("#cpaystep3Modal").on("shown.bs.modal", function () {
        document.getElementById("cpayrfid").value = "";
        document.getElementById("cpayrfid").focus();
        });
    }
}
function cpay_previousStep(step) {
    cpay_currentStep = step;
    cpay_showStep(cpay_currentStep);
}


function ctallyItemCost(){
    sendSelectedValuesCanteen();
}
  




function sendSelectedValuesCanteen() {
    var selectedValues = [];
    $('.operator').each(function() {
        var selectize = $(this)[0].selectize;
        if (selectize && selectize.getValue() !== "") {
            var value = selectize.getValue();
            selectedValues.push(value);
        }
    });

    if (selectedValues.length === 0) {
        // selectedValues is empty
        var errorMessage = "Please Select an Entry";
        var errorContainer = $("#cpay_errorContainerRFID1");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
        );
    } else {
        // selectedValues is not empty
        $.ajax({
        url: "cashdiv_home/tallyItems",
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



function cpay_validateAndProceed() {
    var payrfid = document.getElementById("cpayrfid").value;
    if (payrfid.trim() === "") {
      var errorMessage = "RFID code is required";
      var errorContainer = $("#cpay_errorContainerRFID3");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
      return;
    } else {
      cpay_validate_rfid();
    }
  }


function cpay_validate_rfid() {
var RFID = $("#cpayrfid").val();
var validateRFIDURL = "pos_home/load_rfid_check";
$.ajax({
    url: validateRFIDURL, // Replace with the URL of your Django view
    method: "POST",
    headers: {
    "X-CSRFToken": window.csrfTokenCPay, // Set the CSRF token in the headers
    },
    data: {
    rfid: RFID,
    },
    success: function (response) {
    if (response.exists == 0) {
        // RFID exists in the database and is active
        // Perform the desired action
        // getCreds();
        // load_nextStep(2);
        CRFIDpay(RFID);
    } else {
        // RFID does not exist in the database
        // Perform the desired action
        var errorMessage = "RFID code does not exist";
        var errorContainer = $("#cpay_errorContainerRFID3");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
        );
    }
    },
    error: function (xhr, errmsg, err) {
    var errorMessage = "Please Enter Valid RFID code";
    var errorContainer = $("#cpay_errorContainerRFID3");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
    );
    },
});
}



function CRFIDpay(rfid) {
    var total = $("#FinalTotalAmount").val();
    $.ajax({
        url: "pos_home/payRFID",
        method: "POST",
        headers: {
        "X-CSRFToken": window.csrfTokenCPayRFID, // Set the CSRF token in the headers
        },
        data: {
        rfid: rfid,
        FinalTotalAmount: total,
        },
        success: function (response) {
            if (response.status=='success'){
            var errorMessage = response.message;
            var errorContainer = $("#statusContainer");
            var displayDuration = 5000; // 5 seconds
            displayErrorMessageWithTimer(
            errorMessage,
            errorContainer,
            displayDuration
            );
            // update_Stats();
            $('#cpaystep3Modal').modal('hide');
            } else if (response.status=='error'){
            if (response.status=='error'){
            var errorMessage = response.message;
            var errorContainer = $("#cpay_errorContainerRFID3");
            var displayDuration = 5000; // 5 seconds
            displayErrorMessageWithTimer(
                errorMessage,
                errorContainer,
                displayDuration
            );
            }
        }
        },
        error: function (xhr, status, error) {
            // Handle errors if the request fails
        }
    });
}
