// For loading
var load_currentStep = 1;

function load_validateAndProceed() {
  var loadrfid = document.getElementById("loadrfid").value;
  if (loadrfid.trim() === "") {
    var errorMessage = "RFID code is required.";
    var errorContainer = $("#load_errorContainerRFID");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
    return;
  } else {
    load_validate_rfid();
  }
}

function load_validate_rfid() {
  var RFID = $("#loadrfid").val();
  var validateRFIDURL = "cashdiv_home/load_rfid_check";
  $.ajax({
    url: validateRFIDURL, // Replace with the URL of your Django view
    method: "GET",
    data: {
      rfid: RFID,
    },
    success: function (response) {
      if (response.exists == 0) {
        // RFID exists in the database and is active
        // Perform the desired action
        getCreds();
        load_nextStep(2);
      } else {
        // RFID does not exist in the database
        // Perform the desired action
        var errorMessage = "RFID code does not exist.";
        var errorContainer = $("#load_errorContainerRFID");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
          errorMessage,
          errorContainer,
          displayDuration
        );
      }
    },
    error: function (xhr, errmsg, err) {
      var errorMessage = "Please Enter Valid RFID code.";
      var errorContainer = $("#load_errorContainerRFID");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });
}

function getCreds() {
  var RFID = $("#loadrfid").val();
  var URL = "cashdiv_home/load_rfid_creds";
  $.ajax({
    url: URL, // Replace with the URL of your Django view
    method: "GET",
    data: {
      rfid: RFID,
    },
    success: function (response) {
      // Fetches the credentials of people referenced by RFID code
      var fullname = response.fullname;
      $("#fullname").text(fullname);
      var personID = response.personID;
      $("#personID").text(personID);
    },
    error: function (xhr, errmsg, err) {
      alert("Error, please contact admin.");
    },
  });
}

function payLoad() {
  var RFID = $("#loadrfid").val();
  var amountload = parseFloat($("#amountload").val());
  loadCredAmount(RFID, amountload);
}

function loadCredAmount(rfid, amount) {
  // Prepare the data to be sent in the AJAX request
  var requestData = {
    rfid: rfid,
    amount: amount,
  };

  // Make the AJAX request
  $.ajax({
    url: "cashdiv_home/load_amount",
    type: "GET",
    data: requestData,
    dataType: "json",
    success: function (response) {
      if (response.status === "success") {
        // Handle success response
        var Message = response.message;
        $("#statusContainer").text(Message);
        var displayDuration = 5000;
        setTimeout(function () {
          $("#statusContainer").empty();
        }, displayDuration);
      } else {
        // Handle error response
        var Message = response.message;
        $("#statusContainer").text(Message);
        var displayDuration = 5000;
        setTimeout(function () {
          $("#statusContainer").empty();
        }, displayDuration);
      }
    },
    error: function (xhr, status, error) {
      // Handle AJAX error
      console.error("AJAX Error:", error);
    },
  });
}

function showTotal_TopUp() {
  var amountload = parseFloat($("#amountload").val());
  $("#basetopup").text(amountload);
  $("#bonustopup").text(amountload * 0.05);
  $("#totaltopup").text(amountload * 1.05);
}

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

function load_showStep(step) {
  $(".modal").modal("hide");
  $("#loadstep" + step + "Modal").modal("show");
}

function load_nextStep(step) {
  load_currentStep = step;
  load_showStep(load_currentStep);
  if (step == 1) {
    $("#loadstep1Modal").on("shown.bs.modal", function () {
      document.getElementById("loadrfid").value = "";
      document.getElementById("loadrfid").focus();
    });
  } else if (step == 3) {
    showTotal_TopUp();
  }
}
function load_previousStep(step) {
  load_currentStep = step;
  load_showStep(load_currentStep);
}

$(document).ready(function () {
  $("#loadstep1Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#loadbuttontarget").click();
    }
  });
});
$(document).ready(function () {
  $("#loadstep2Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#loadbuttontarget2").click();
    }
  });
});
$(document).ready(function () {
  $("#loadstep3Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#loadbuttontarget3").click();
    }
  });
});

// for the registration
var currentStep = 1;
function validateAndProceed() {
  var regStudentID = document.getElementById("regStudentID").value;
  if (regStudentID.trim() === "") {
    var errorMessage = "Please Enter a Student ID.";
    var errorContainer = $("#errorContainer");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
    return;
  } else {
    validate_SID();
  }
}

function showStep(step) {
  $(".modal").modal("hide");
  $("#regstep" + step + "Modal").modal("show");
}

function nextStep(step) {
  currentStep = step;
  showStep(currentStep);
  if (step == 3) {
    var regStudentID = document.getElementById("regStudentID").value;
    var currentSchoolIDElement = document.getElementById("currentschoolid");
    currentSchoolIDElement.innerText = regStudentID;
  }
}
function previousStep(step) {
  currentStep = step;
  showStep(currentStep);
}
function validate_SID() {
  var studentID = $("#regStudentID").val();
  var validateSIDUrl = "cashdiv_home/register_sid_check";
  $.ajax({
    url: validateSIDUrl, // Replace with the URL of your Django view
    method: "GET",
    data: {
      school_id: studentID,
    },
    success: function (response) {
      if (response.exists == 2) {
        // Student ID exists in the database and is active
        // Perform the desired action
        nextStep(2);

        $("#regstep2Modal").on("shown.bs.modal", function () {
          document.getElementById("rfid").value = "";
          document.getElementById("rfid").focus();
        });
      } else if (response.exists == 3) {
        // Student ID exists in the database and is active
        // Perform the desired action
        var errorMessage = "Student ID is already in use!";
        var errorContainer = $("#errorContainer");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
          errorMessage,
          errorContainer,
          displayDuration
        );
      } else if (response.exists == 0) {
        // Student ID does not exist in the database
        // Perform the desired action
        var errorMessage = "Student ID does not Exist!";
        var errorContainer = $("#errorContainer");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
          errorMessage,
          errorContainer,
          displayDuration
        );
      }
    },
    error: function (xhr, errmsg, err) {
      var errorMessage = "Please Enter a valid ID number.";
      var errorContainer = $("#errorContainer");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });
}

function validate_rfid() {
  var RFID = $("#rfid").val();
  var validateRFIDURL = "cashdiv_home/register_rfid_check";
  $.ajax({
    url: validateRFIDURL, // Replace with the URL of your Django view
    method: "GET",
    data: {
      rfid: RFID,
    },
    success: function (response) {
      if (response.exists == 0) {
        // RFID exists in the database and is active
        // Perform the desired action
        nextStep(3);
      } else {
        // RFID does not exist in the database
        // Perform the desired action
        var errorMessage = "Please Enter Valid RFID code.";
        var errorContainer = $("#errorContainerRFID");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
          errorMessage,
          errorContainer,
          displayDuration
        );
      }
    },
    error: function (xhr, errmsg, err) {
      var errorMessage = "Please Enter Valid RFID code.";
      var errorContainer = $("#errorContainerRFID");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });
}
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

function registerRFID() {
  var school_id = $("#regStudentID").val();
  var rfid = $("#rfid").val();
  var register_rfid = "cashdiv_home/register_rfid";
  $.ajax({
    url: register_rfid, // Replace with your Django view URL
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrfToken, // Set the CSRF token in the headers
    },
    data: {
      school_id: school_id,
      rfid: rfid,
    },
    success: function (response) {
      // Handle successful form submission
      // You can show a success message or redirect the user
      var Message = response.message;
      $("#statusContainer").text(Message);
      var displayDuration = 5000;
      setTimeout(function () {
        $("#statusContainer").empty();
      }, displayDuration);
    },
    error: function (xhr, errmsg, err) {
      // Handle the error case
      console.log(errmsg); // Log the error message to the console

      // Display an error message to the user
      var errorMessage =
        "An error occurred while validating the RFID code. Please try again later.";
      // You can display the error message in an alert box or update an HTML element with the error message.
      // For example, assuming you have an element with the ID 'errorContainer':
      $("#errorContainer").text(errorMessage);
      var displayDuration = 1000;
      setTimeout(function () {
        $("#errorContainer").empty();
      }, displayDuration);
    },
  });
}

$(document).ready(function () {
  $("#regstep1Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#regbuttontarget").click();
    }
  });
});
$(document).ready(function () {
  $("#regstep2Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#regbuttontarget2").click(); // Trigger the "Register" button click event
    }
  });
});
$(document).ready(function () {
  $("#regstep3Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#regbuttontarget3").click(); // Trigger the "Register" button click event
    }
  });
});

// Function to close the active modal
function closeModal() {
  var activeModal = document.querySelector(".modal.show");
  if (activeModal) {
    var modalInstance = bootstrap.Modal.getInstance(activeModal);
    modalInstance.hide();
  }
}

// Function to handle key press event
function handleKeyPress(event) {
  // Check if the pressed key is the Escape key
  if (event.key === "Escape") {
    closeModal(); // Call the function to close the active modal
  }
}

// Add event listener to the keydown event on the document
document.addEventListener("keydown", handleKeyPress);
