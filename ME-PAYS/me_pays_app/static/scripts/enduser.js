

function displayErrorMessageWithTimer(
    errorMessage,
    containerElement,
    duration
  ) {
    containerElement.text(errorMessage);
    setTimeout(function () {
      containerElement.empty();
    }, duration);
  }

function clearInput(){
    $("#amount").val("");
}

function share_validateAndProceed() {
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
        share_validate_sid();
    }
}
  
function share_validate_sid() {
    var school_id = $("#idnumber").val();
    var validateURL = "home/validateshare";
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
            shareGetCreds();
            share_nextStep(2);
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





function SendAmount() {
    // Prepare the data to be sent in the AJAX request
    var sid = $("#idnumber").val();
    var amount = parseFloat($("#amount").val());
    var requestData = {
      sid: sid,
      amount: amount,
    };
    // Make the AJAX request
    $.ajax({
      url: "home/share_send",
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
          update_Balance();
          $('#sharestep2Modal').modal('hide');
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











function shareGetCreds() {
    var school_id = $("#idnumber").val();
    var URL = "home/share_get_creds";
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

var share_currentStep = 1;

function share_showStep(step) {
    $(".modal").modal("hide");
    $("#sharestep" + step + "Modal").modal("show");
}
function share_nextStep(step) {
    share_currentStep = step;
    share_showStep(share_currentStep);
}

function share_previousStep(step) {
    share_currentStep = step;
    share_showStep(share_currentStep);
}



function update_Balance() {
    $.ajax({
        url: 'home/get_balance',  // Replace with the URL of your AJAX endpoint
        method: 'GET',
        success: function(response) {
            // Update the values with the response data
            $('#balance').text(response.balance.toFixed(1));
        },
        error: function() {
            console.log('Error occurred during AJAX request.');
        }
    });
}