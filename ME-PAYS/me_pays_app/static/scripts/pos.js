
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








function sendSelectedValuesCanteen() {
    var selectedValues = [];
    $('.operator').each(function() {
        var selectize = $(this)[0].selectize;
        if (selectize && selectize.getValue() !== "") {
            var value = selectize.getValue();
            var divId = $(this).attr('id');
            var qty = $('#' + divId + 'qty').val(); 
            selectedValues.push([value, qty]);
        }
    });
    
    console.log(selectedValues);
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

function pos_share_validateAndProceed() {
    var school_id = document.getElementById("idnumber").value;
    var amount = document.getElementById("amount").value;
    if (school_id.trim() === "" && amount.trim() === "") {
        var errorMessage = "Please Input Transaction Info";
        var errorContainer = $("#share_errorContainer");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
        return;
    } 
    else if (school_id.trim() === ""){
        var errorMessage = "Please Input The ID Number of Recipient";
        var errorContainer = $("#share_errorContainer");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
        return;
    }
    else if (amount.trim() === ""){
        var errorMessage = "Please Input The Amount";
        var errorContainer = $("#share_errorContainer");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
        return;
    }
    else {
        pos_share_validate_sid();
    }
}

function pos_share_validate_sid() {
    var school_id = $("#idnumber").val();
    var validateURL = "pos_home/validateshare";
    $.ajax({
      url: validateURL, // Replace with the URL of your Django view
      method: "POST",
      headers: {
        "X-CSRFToken": window.csrfTokenShareValidate, // Set the CSRF token in the headers
      },
      data: {
        school_id: school_id,
      },
      success: function (response) {
        if (response.exists == 1) {
          // SID exists in the database and is active
          // Perform the desired action
            pos_shareGetCreds();
            pos_share_nextStep(2);
        } else { 
          // SID does not exist in the database
          // Perform the desired action
          var errorMessage = "ID number does not exist";
          var errorContainer = $("#share_errorContainer");
          var displayDuration = 5000; // 5 seconds
          displayErrorMessageWithTimer(
            errorMessage,
            errorContainer,
            displayDuration
          );
        }
      },
      error: function (xhr, errmsg, err) {
        var errorMessage = "Please enter a valid ID number";
        var errorContainer = $("#share_errorContainer");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
          errorMessage,
          errorContainer,
          displayDuration
        );
      },
    });
}

function pos_SendAmount() {
    // Prepare the data to be sent in the AJAX request
    var sid = $("#idnumber").val();
    var amount = parseFloat($("#amount").val());
    var requestData = {
      sid: sid,
      amount: amount,
    };
    // Make the AJAX request
    $.ajax({
      url: "pos_home/share_send",
      method: "POST",
      headers: {
        "X-CSRFToken": window.csrfTokenSharePay // Set the CSRF token in the headers
      },
      data: requestData,
      success: function (response) {
        if (response.status === "success") {
          // Handle success response
          var Message = response.message;
          $("#statusContainer").text(Message);
          var displayDuration = 5000;
          setTimeout(function () {
            $("#statusContainer").empty();
          }, displayDuration);
          $('#pos_sharestep2Modal').modal('hide');
        } else {
          // Handle error response
          var Message = response.message;
          $("#share_errorContainer2").text(Message);
          var displayDuration = 5000;
          setTimeout(function () {
            $("#share_errorContainer2").empty();
          }, displayDuration);
        }
      },
      error: function (xhr, status, error) {
        // Handle AJAX error
        console.error("AJAX Error:", error);
      },
    });
}





function pos_shareGetCreds() {
    var school_id = $("#idnumber").val();
    var URL = "pos_home/share_get_creds";
    $.ajax({
      url: URL, // Replace with the URL of your Django view
      method: "GET",
      data: {
        school_id: school_id,
      },
      success: function (response) {
        // Fetches the credentials of people referenced by RFID code
        var fullname = response.fullname;
        $("#fullname").val(fullname);
        var personID = response.personID;
        $("#personID").val(personID);
        var amount = $("#amount").val();
        $("#amountshow").val(amount);
      },
      error: function (xhr, errmsg, err) {
        alert("Error, please contact admin.");
      },
    });
}

var pos_share_currentStep = 1;

function pos_share_showStep(step) {
    $(".modal").modal("hide");
    $("#pos_sharestep" + step + "Modal").modal("show");
}
function pos_share_nextStep(step) {
    pos_share_currentStep = step;
    pos_share_showStep(pos_share_currentStep);
}

function pos_share_previousStep(step) {
    pos_share_currentStep = step;
    pos_share_showStep(pos_share_currentStep);
}