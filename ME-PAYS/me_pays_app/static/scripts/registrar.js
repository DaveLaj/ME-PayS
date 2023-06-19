
var registrar_currentStep = 2;

function registrar_showStep(step) {
    $(".modal").modal("hide");
    $("#registrarstep" + step + "Modal").modal("show");

    if (step === 3) {
        // Create a confetti instance
        var confettiSettings = {
          target: 'registrarstep3Modal .modal-content',
          max: 100,   // Number of confetti particles
          size: 1,    // Size of confetti particles
          animate: true
        };
        var confetti = new ConfettiGenerator(confettiSettings);
    
        // Start the confetti animation
        confetti.render();
    }
  }
  
  function registrar_nextStep(step) {
    registrar_currentStep = step;
    registrar_showStep(registrar_currentStep);
  }
  function registrar_previousStep(step) {
    registrar_currentStep = step;
    registrar_showStep(registrar_currentStep);
  }



function registrar_validate_SID() {
    var studentID = $("#registrarSID").val();
    var validateSIDUrl = "registrar_home/validateSID";
    $.ajax({
        url: validateSIDUrl, // Replace with the URL of your Django view
        method: "GET",
        data: {
        school_id: studentID,
        },
        success: function (response) {
            if (response.exists == 1) {
                // Student ID exists in the database and is active
                // Perform the desired action
                TallySelectedValuesRegistrar();
                
            } else if (response.exists == 0) {
                var errorMessage = "Please enter an existing number";
                var errorContainer = $("#registrar_errorContainer1");
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
        var errorContainer = $("#registrar_errorContainer1");
        var displayDuration = 5000; // 5 seconds
        displayErrorMessageWithTimer(
            errorMessage,
            errorContainer,
            displayDuration
        );
        },
    });
}





var selectedValues = [];
function TallySelectedValuesRegistrar() {
    selectedValues = [];
    var shouldExit = false;
    $('.operator').each(function() {
        var selectize = $(this)[0].selectize;
        if (selectize && selectize.getValue() !== "") {
            var value = selectize.getValue();
            var text = selectize.options[value].text; // Get the select option text
            var id = $(this).attr('id');
            var qty = $('#' + id + 'qty').val();
            if (qty !== ''){
                selectedValues.push([value,qty,text]); // Add the option text to the selectedValues array
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
            SID = $('#registrarSID').val();
            $('#show_registrarSID').text(SID);
            $('#showTally').empty();
            $('#totalAmount').empty();
            $('#FinalTotalAmount').val('');
            itemData.forEach(function(item) {
              printTallyRegistrar(item.id, item.name, item.price, item.quantity);
              // Perform operations with the item data
              // total all prices
              priceTotal += parseInt(item.price);
            });
            document.getElementById("totalAmount").innerText = "Php "+priceTotal.toString();
            var TotalAmount = document.getElementById('FinalTotalAmount');
            TotalAmount.value = parseInt(priceTotal);
            registrar_nextStep(2);
          },
          error: function(xhr, status, error) {
            // Handle the error if the request fails
            console.error("AJAX request failed:", error);
          }
        });
        
    }


}



function sendSelectedValuesRegistrar() {
    var studentID = $("#registrarSID").val();
    $.ajax({
    url: "registrar_home/sendItems",
    method: "POST",
    headers: {
        "X-CSRFToken": window.csrfTokenPay, // Set the CSRF token in the headers
    },
    data: { selectedValues: JSON.stringify(selectedValues),
            school_id: studentID
    },
    success: function(response) {
        // Handle the success response
        // Parse the serialized data
        var refnum = response.refnum;
        $('#refnum').text(refnum);
        $('#registrarSID').val('');
        registrar_nextStep(3);
    },
    error: function(xhr, status, error) {
        // Handle the error if the request fails
        console.error("AJAX request failed:", error);
    }
    });
    
}