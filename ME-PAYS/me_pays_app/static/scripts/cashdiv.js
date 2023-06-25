// For loading ===========================================================================================================
var load_currentStep = 1;
function load_validateAndProceed() {
  var loadrfid = document.getElementById("loadrfid").value;
  if (loadrfid.trim() === "") {
    var errorMessage = "RFID code is required";
    var errorContainer = $("#load_errorContainerRFID2");
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
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrfTokenLoad, // Set the CSRF token in the headers
    },
    data: {
      rfid: RFID,
    },
    success: function (response) {
      if (response.exists == 0) {
        // RFID exists in the database and is active
        // Perform the desired action
        getCreds();
        load_nextStep(3);
      } else {
        // RFID does not exist in the database
        // Perform the desired action
        var errorMessage = "RFID code does not exist";
        var errorContainer = $("#load_errorContainerRFID2");
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
      var errorContainer = $("#load_errorContainerRFID2");
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



function load_amountValidate() {
  var amountload = parseFloat($("#amountload").val());
  if (isNaN(amountload)) {
    var errorMessage = "Please Enter an Amount";
    var errorContainer = $("#load_errorContainerRFID");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
  }
  else if (amountload < 0) {
    var errorMessage = "Cannot Accept Negative Number";
    var errorContainer = $("#load_errorContainerRFID");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(
      errorMessage,
      errorContainer,
      displayDuration
    );
  } else {
    load_nextStep(2);
  }

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
    method: "GET",
    headers: {
      "X-CSRFToken": window.csrfToken, // Set the CSRF token in the headers
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
        update_Stats();
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
  if (step == 2) {
    $("#loadstep2Modal").on("shown.bs.modal", function () {
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



$(document).ready(function () {
  $("#paystep1Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#paybuttontarget").click();
    }
  });
});
$(document).ready(function () {
  $("#paystep2Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#changebutton").click();
    }
  });
});
$(document).ready(function () {
  $("#paystep3Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#paybuttontarget3").click();
    }
  });
});
$(document).ready(function () {
  $("#paystep4Modal").keyup(function (event) {
    if (event.keyCode === 13) {
      // Enter key pressed
      $("#paybuttontarget4").click();
    }
  });
});


// For cashout ========================================================================================================================

var cashout_currentStep = 1;


function cashout_showStep(step) {
  $(".modal").modal("hide");
  $("#cashoutstep" + step + "Modal").modal("show");
}

function cashout_nextStep(step) {
  cashout_currentStep = step;
  cashout_showStep(cashout_currentStep);
  if (step == 1) {
    $("#cashoutstep1Modal").on("shown.bs.modal", function () {
      document.getElementById("cashoutrfid").value = "";
      document.getElementById("cashoutrfid").focus();
    });
  } else if (step == 3) {
    cashout_showTotal_TopUp();
  }
}

function cashout_showTotal_TopUp() {
  var amountload = parseFloat($("#cashout_amountload").val());
  $("#basetopup_cashout").text(amountload);
}



function cashout_previousStep(step) {
  cashout_currentStep = step;
  cashout_showStep(cashout_currentStep);
}


function cashout_validateAndProceed() {
  var cashoutrfid = document.getElementById("cashoutrfid").value;
  if (cashoutrfid.trim() === "") {
    var errorMessage = "RFID code is required";
    var errorContainer = $("#cashout_errorContainerRFID1");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
    return;
  } else {
    cashout_validate_rfid();
  }
}



function cashout_validate_rfid() {
  var RFID = $("#cashoutrfid").val();
  var validateRFIDURL = "cashdiv_home/cashout_rfid_check";
  $.ajax({
    url: validateRFIDURL, // Replace with the URL of your Django view
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrfTokenCashout, // Set the CSRF token in the headers
    },
    data: {
      rfid: RFID,
    },
    success: function (response) {
      if (response.exists == 0) {
        // RFID exists in the database and is active
        // Perform the desired action
        cashout_getCreds();
        cashout_nextStep(2);
      } else {
        // RFID does not exist in the database
        // Perform the desired action
        var errorMessage = "RFID code does not exist";
        var errorContainer = $("#cashout_errorContainerRFID1");
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
      var errorContainer = $("#cashout_errorContainerRFID1");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });
}

function cashout_getCreds() {
  var RFID = $("#cashoutrfid").val();
  var URL = "cashdiv_home/cashout_rfid_creds";
  $.ajax({
    url: URL, // Replace with the URL of your Django view
    method: "GET",
    data: {
      rfid: RFID,
    },
    success: function (response) {
      // Fetches the credentials of people referenced by RFID code
      var balance = response.balance;
      $("#currentbal_cashout").text(balance);
      var fullname = response.fullname;
      $("#fullname_cashout").text(fullname);
      var personID = response.personID;
      $("#personID_cashout").text(personID);
    },
    error: function (xhr, errmsg, err) {
      alert("Error, please contact admin.");
    },
  });
}


function validate_balance () {
  var rfid = $("#cashoutrfid").val();
  var amount = parseFloat($("#cashout_amountload").val());
  var requestData = {
    rfid: rfid,
    amount: amount,
  };
  $.ajax({
    url: "cashdiv_home/verify_bal",
    method: "GET",
    data: requestData,
    success: function (response) {
      if (response.status === "success") {
        // Handle success response
        cashout_nextStep(3);
      } else {
        var Message = response.message;
        $("#cashout_errorContainerRFID2").text(Message);
        var displayDuration = 5000;
        setTimeout(function () {
          $("#cashout_errorContainerRFID2").empty();
        }, displayDuration);
      }
    },
    error: function (xhr, status, error) {
      // Handle AJAX error
      console.error("AJAX Error:", error);
    },
  });
  
}









function cashout() {
  var RFID = $("#cashoutrfid").val();
  var amountcashout = parseFloat($("#cashout_amountload").val());
  cashoutCredAmount(RFID, amountcashout);
}

function cashoutCredAmount(rfid, amount) {
  // Prepare the data to be sent in the AJAX request
  var requestData = {
    rfid: rfid,
    amount: amount,
  };
  // Make the AJAX request
  $.ajax({
    url: "cashdiv_home/cashout_amount",
    method: "GET",
    headers: {
      "X-CSRFToken": window.csrfTokenCashoutFinal, // Set the CSRF token in the headers
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

















// for the registration================================================================================================================
var currentStep = 1;
function validateAndProceed() {
  var regStudentID = document.getElementById("regStudentID").value;
  if (regStudentID.trim() === "") {
    var errorMessage = "Please Enter a Student ID";
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
      var errorMessage = "Please Enter a valid ID number";
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
    url: validateRFIDURL,
    method: "GET",
    data: {
      rfid: RFID,
    },
    success: function (response) {
      if (response.exists == 0) {
        // RFID does not exist
        // Perform the desired action
        nextStep(3);
      } else {
        // RFID does not exist in the database
        // RFID already exists in DB
        // Perform the desired action
        var errorMessage = "RFID code is already in use!";
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
      var errorMessage = "Please Enter Valid RFID code";
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
      "X-CSRFToken": window.csrfTokenReg, // Set the CSRF token in the headers
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







// Payment Functions ===========================================================================================
var pay_currentStep = 1;

function pay_showStep(step) {
  $(".modal").modal("hide");
  $("#paystep" + step + "Modal").modal("show");
}




function pay_nextStep(step) {
  pay_currentStep = step;
  pay_showStep(pay_currentStep);
  if (step == 4) {
    $("#paystep4Modal").on("shown.bs.modal", function () {
      document.getElementById("payrfid").value = "";
      document.getElementById("payrfid").focus();
    });
  }
}
function pay_previousStep(step) {
  pay_currentStep = step;
  pay_showStep(pay_currentStep);
}

function clearRefNum() {
  $("#paystep1Modal").on("shown.bs.modal", function () {
    document.getElementById("payfees_school_id").value = "";
    document.getElementById("payfees_school_id").focus();
  });
}



function getCart() {
  var school_id = $("#payfees_school_id").val();
  var URL = "cashdiv_home/getCart";
  $.ajax({
    url: URL, // Replace with the URL of your Django view
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrfTokengetCart, // Set the CSRF token in the headers
    },
    data: {
      school_id: school_id,
    },
    success: function (response) {
      // Print cart information\
      $('#showCart').empty();
      $("#show_school_id").text(school_id)
      var orderlist = response.orderlist;
      for (var i = 0; i < orderlist.length; i++) {
        var order = orderlist[i];
        // Access the fields of each order
        var referenceNumber = order.fields.reference_number;
        var paid = order.fields.paid;
        var datetimeString = order.fields.datetime;
        var options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
        var formattedDatetime = new Date(datetimeString).toLocaleString('en-US', options);
        // Perform further processing with the order data
        printCart(referenceNumber, paid, formattedDatetime);
      }
      pay_nextStep(2);
    },
    error: function (xhr, errmsg, err) {
      var errorMessage = "Please enter a valid School ID";
      var errorContainer = $("#pay_errorContainerRFID1");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });
}


function pay_clean_school_id() {
  var school_id = $("#payfees_school_id").val();
  if (school_id.trim() === "") {
    var errorMessage = "School ID is required";
    var errorContainer = $("#pay_errorContainerRFID1");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
    return;
  } else {
    pay_validate_school_id();
  }
}



function pay_validate_school_id() {
  var school_id = $("#payfees_school_id").val();
  var URL = "cashdiv_home/pay_validate_school_id";
  $.ajax({
    url: URL, // Replace with the URL of your Django view
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrfTokenRefNum, // Set the CSRF token in the headers
    },
    data: {
      school_id: school_id,
    },
    success: function (response) {
      if (response.exists == 1) {
        var errorMessage = "School ID doesn't Exist";
        var errorContainer = $("#pay_errorContainerRFID1");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
          errorMessage,
          errorContainer,
          displayDuration
        );
      
      } else if(response.exists == 2){
        getCart();
       
      } else {
        var errorMessage = "School ID doesn't Have any pending requests";
        var errorContainer = $("#pay_errorContainerRFID1");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
          errorMessage,
          errorContainer,
          displayDuration
        );
      } 
    },
    error: function (xhr, errmsg, err) {
      var errorMessage = "Please Enter a valid School ID";
      var errorContainer = $("#pay_errorContainerRFID1");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });
}

function cashier_order_info(refnum) {
  funcURL = "cashdiv_home/order_info";
  $.ajax({
    url: funcURL, // Replace with the URL of your Django view
    method: "GET",
    data: {
      refnum: refnum,
    },
    success: function (response) {
      $("#refnum").val(refnum);
      $('#showTally').empty();
      $('#totalAmount').empty();
      $('#FinalTotalAmount').val('');
      document.getElementById("totalAmount").innerText = response.total_price;
      document.getElementById("show_refnum").innerText = response.reference_number;
      document.getElementById("show_sid").innerText = response.student_id;
      $('#FinalTotalAmount').val(response.total_price);
      var cart = JSON.parse(response.cart);
      for (var i = 0; i < cart.length; i++) {
        var item = cart[i];
        var id = item.id;
        var name = item.name;
        var price = item.price;
        var qty = item.qty;
        printTally(id, name, price, qty)
      }
      pay_nextStep(3);
    },
    error: function (xhr, errmsg, err) {
      var errorMessage = "Error please call admin";
      var errorContainer = $("#pay_errorContainerRFID3");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });

}




function pay_validateAndProceed() {
  var payrfid = document.getElementById("payrfid").value;
  if (payrfid.trim() === "") {
    var errorMessage = "RFID code is required";
    var errorContainer = $("#pay_errorContainerRFID4");
    var displayDuration = 5000; // 5 seconds
    displayErrorMessageWithTimer(errorMessage, errorContainer, displayDuration);
    return;
  } else {
    pay_validate_rfid();
  }
}


function pay_validate_rfid() {
  var RFID = $("#payrfid").val();
  var validateRFIDURL = "cashdiv_home/load_rfid_check";
  $.ajax({
    url: validateRFIDURL, // Replace with the URL of your Django view
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrfTokenPay, // Set the CSRF token in the headers
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
        RFIDpay(RFID);
      } else {
        // RFID does not exist in the database
        // Perform the desired action
        var errorMessage = "RFID code does not exist";
        var errorContainer = $("#pay_errorContainerRFID4");
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
      var errorContainer = $("#pay_errorContainerRFID4");
      var displayDuration = 5000; // 5 seconds
      displayErrorMessageWithTimer(
        errorMessage,
        errorContainer,
        displayDuration
      );
    },
  });
}


// RFID pay
function RFIDpay(rfid) {
  var refnum = $("#refnum").val();
  var total = $("#FinalTotalAmount").val();
  $.ajax({
    url: "cashdiv_home/payRFID",
    method: "POST",
    headers: {
      "X-CSRFToken": window.csrfTokenPayRFID, // Set the CSRF token in the headers
    },
    data: {
      rfid: rfid,
      FinalTotalAmount: total,
      refnum : refnum,
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
        update_Stats();
        $('#paystep4Modal').modal('hide');
       } else if (response.status=='error'){
        if (response.status=='error'){
          var errorMessage = response.message;
          var errorContainer = $("#pay_errorContainerRFID4");
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




function update_Stats() {
  $.ajax({
      url: 'cashdiv_home/updateStats',  // Replace with the URL of your AJAX endpoint
      method: 'GET',
      success: function(response) {
          // Update the values with the response data
          $('#cash-in-count').text(response.dailyCashInCount);
          $('#total-cash-in').text(response.dailyTotalCashIn.toFixed(1));
          $('#pay-count').text(response.dailyPayCount);
          $('#total-pay').text(response.dailyTotalPay.toFixed(1));
      },
      error: function() {
          console.log('Error occurred during AJAX request.');
      }
  });
}


