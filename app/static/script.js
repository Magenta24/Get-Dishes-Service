function customerShowTimeSelect() {
    document.getElementById("location").style.display = "none";
    document.getElementById("booking-time").style.display = "block";
    document.getElementById("confirmation").style.display = "none";

    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.add("active");
    document.getElementById("third-dot").classList.remove("active");
}

function customerBackLocationSelect() {
    document.getElementById("location").style.display = "block";
    document.getElementById("booking-time").style.display = "none";
    document.getElementById("confirmation").style.display = "none";

    document.getElementById("first-dot").classList.add("active");
    document.getElementById("second-dot").classList.remove("active");
    document.getElementById("third-dot").classList.remove("active");
}

function customerCheckBeforeConfirmation() {
    // before we go to confirmation it would be worth checking for empty fields in form

    var bookScooter = document.getElementById("book_scooter");

    var pickUp = bookScooter.elements["pick_up_location"];
    var dropOff = bookScooter.elements["drop_off_location"];
    var pickDate = bookScooter.elements["pick_up_date"];
    var pickTime = bookScooter.elements["pick_up_time"];
    var rideDuration = bookScooter.elements["ride_duration"];

    // a bit clumsy but it works as value is returned as string
    // if anything is empty we don't go further so the form gets correct info
    if (
        pickUp.value == "" ||
        dropOff.value == "" ||
        pickDate.value == "" ||
        pickTime.value == "" ||
        rideDuration.value == ""
    ) {
        document.getElementById("error-form").style.display = "block";
    } else {
        document.getElementById("error-form").style.display = "none";
        customerShowConfirmation();
    }
}

function customerShowConfirmation() {
    var bookScooter = document.getElementById("book_scooter");
    var pickUp = bookScooter.elements["pick_up_location"];
    var dropOff = bookScooter.elements["drop_off_location"];
    var pickDate = bookScooter.elements["pick_up_date"];
    var pickTime = bookScooter.elements["pick_up_time"];
    var rideDuration = bookScooter.elements["ride_duration"];

    document.getElementById("confirm_pick_up_loc").innerHTML = pickUp.selectedOptions[0].text;
    document.getElementById("confirm_drop_off_loc").innerHTML = dropOff.selectedOptions[0].text;
    document.getElementById("confirm_pick_up_date").innerHTML = pickDate.value;
    document.getElementById("confirm_pick_up_time").innerHTML = pickTime.value;
    document.getElementById("confirm_ride_duration").innerHTML = rideDuration.selectedOptions[0].text;

    document.getElementById("booking-time").style.display = "none";
    document.getElementById("location").style.display = "none";
    document.getElementById("confirmation").style.display = "block";

    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.remove("active");
    document.getElementById("third-dot").classList.add("active");
}

function customerBackTimeSelect() {
    document.getElementById("location").style.display = "none";
    document.getElementById("confirmation").style.display = "none";
    document.getElementById("booking-time").style.display = "block";

    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.add("active");
    document.getElementById("third-dot").classList.remove("active");
}


// employee view, booking for unregistered users code
function showTimeSelect() {
    document.getElementById("location").style.display = "none";
    document.getElementById("booking-time").style.display = "block";
    document.getElementById("confirmation").style.display = "none";
    document.getElementById("customer-details").style.display = "none";


    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.add("active");
    document.getElementById("third-dot").classList.remove("active");
    document.getElementById("fourth-dot").classList.remove("active");
}

function backToLocationSelect() {
    document.getElementById("location").style.display = "block";
    document.getElementById("booking-time").style.display = "none";
    document.getElementById("confirmation").style.display = "none";
    document.getElementById("customer-details").style.display = "none";


    document.getElementById("first-dot").classList.add("active");
    document.getElementById("second-dot").classList.remove("active");
    document.getElementById("third-dot").classList.remove("active");
    document.getElementById("fourth-dot").classList.remove("active");
}

function CheckBeforeCustomerDetails() {
    // before we go to confirmation it would be worth checking for empty fields in form

    var bookScooter = document.getElementById("book_scooter");

    var pickUp = bookScooter.elements["pick_up_location"];
    var dropOff = bookScooter.elements["drop_off_location"];
    var pickDate = bookScooter.elements["pick_up_date"];
    var pickTime = bookScooter.elements["pick_up_time"];
    var rideDuration = bookScooter.elements["ride_duration"];

    // a bit clumsy but it works as value is returned as string
    // if anything is empty we don't go further so the form gets correct info
    if (
        pickUp.value == "" ||
        dropOff.value == "" ||
        pickDate.value == "" ||
        pickTime.value == "" ||
        rideDuration.value == ""
    ) {
        document.getElementById("error-form").style.display = "block";
    } else {
        document.getElementById("error-form").style.display = "none";
        goToCustomerDetails();
    }
}

function checkBeforeConfirmation() {
    // before we go to confirmation it would be worth checking for empty fields in form

    var bookScooter = document.getElementById("book_scooter");

    var customerName = bookScooter.elements["customer_name"];
    var customerSurname = bookScooter.elements["customer_surname"];
    var customerEmail = bookScooter.elements["customer_email"];

    // a bit clumsy but it works as value is returned as string
    // if anything is empty we don't go further so the form gets correct info

    if (
        customerName.value == "" ||
        customerSurname.value == "" ||
        customerEmail.value == ""
    ) {
        document.getElementById("error-form-em").style.display = "block";
    } else {
        document.getElementById("error-form-em").style.display = "none";
        showConfirmation();
    }
}

function showConfirmation() {
    document.getElementById("booking-time").style.display = "none";
    document.getElementById("location").style.display = "none";
    document.getElementById("confirmation").style.display = "block";
    document.getElementById("customer-details").style.display = "none";
    // document.getElementById("booking-time").style.display = "none";

    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.remove("active");
    document.getElementById("third-dot").classList.remove("active");
    document.getElementById("fourth-dot").classList.add("active");

    var bookScooter = document.getElementById("book_scooter");
    var pickUp = bookScooter.elements["pick_up_location"];
    var dropOff = bookScooter.elements["drop_off_location"];
    var pickDate = bookScooter.elements["pick_up_date"];
    var pickTime = bookScooter.elements["pick_up_time"];
    var rideDuration = bookScooter.elements["ride_duration"];

    var customerName = bookScooter.elements["customer_name"];
    var customerSurname = bookScooter.elements["customer_surname"];
    var customerEmail = bookScooter.elements["customer_email"];

    document.getElementById("confirm_pick_up_loc").innerHTML = pickUp.selectedOptions[0].text;
    document.getElementById("confirm_drop_off_loc").innerHTML = dropOff.selectedOptions[0].text;
    document.getElementById("confirm_pick_up_date").innerHTML = pickDate.value;
    document.getElementById("confirm_pick_up_time").innerHTML = pickTime.value;
    document.getElementById("confirm_ride_duration").innerHTML = rideDuration.selectedOptions[0].text;

    document.getElementById("confirm_name").innerHTML = customerName.value;
    document.getElementById("confirm_surname").innerHTML = customerSurname.value;
    document.getElementById("confirm_email").innerHTML = customerEmail.value;
}

function backToTimeSelect() {
    document.getElementById("location").style.display = "none";
    document.getElementById("confirmation").style.display = "none";
    document.getElementById("customer-details").style.display = "none";
    document.getElementById("booking-time").style.display = "block";

    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.add("active");
    document.getElementById("third-dot").classList.remove("active");
}

function backToCustomerDetails() {
    document.getElementById("location").style.display = "none";
    document.getElementById("booking-time").style.display = "none";
    document.getElementById("confirmation").style.display = "none";
    document.getElementById("customer-details").style.display = "block";

    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.remove("active");
    document.getElementById("third-dot").classList.add("active");
    document.getElementById("fourth-dot").classList.remove("active");
}

function goToCustomerDetails() {
    document.getElementById("location").style.display = "none";
    document.getElementById("confirmation").style.display = "none";
    document.getElementById("booking-time").style.display = "none";
    document.getElementById("customer-details").style.display = "block";

    document.getElementById("first-dot").classList.remove("active");
    document.getElementById("second-dot").classList.remove("active");
    document.getElementById("third-dot").classList.add("active");
    document.getElementById("fourth-dot").classList.remove("active");
}


// MANAGER MANAGE RENTAL COSTS FUNCTION
function changeRentalCost(index) {
    var collapsibleContent = document.getElementById("collapsible-content-" + index);
    var collapsibleButton = document.getElementById("collapsible-button-" + index);

    if (collapsibleContent.style.display == "none") {
        collapsibleContent.style.display = "block";
        collapsibleButton.innerHTML = "Back";
        collapsibleButton.classList.remove('btn-dark');
        collapsibleButton.classList.add('btn-dark');
    } else {
        collapsibleContent.style.display = "none";
        collapsibleButton.innerHTML = "Change";
        collapsibleButton.classList.remove('btn-green');
        collapsibleButton.classList.add('btn-dark');
    }
}
