/// notes :  update ui with loder while sending requests to backend
import { fetchRequest } from "./FetchRequest.js";
import { isValidateUSerInput } from "./ValidateInput.js";
import {
  displayErrorAtElement,
  buildValidationErrorMessage,
} from "./HandelErrors.js";
import { hideModal, showOTPModal } from "./Modal.js";

const firstName = document.getElementById("first_name");
const lastName = document.getElementById("last_name");
const email = document.getElementById("email");
const phone = document.getElementById("phone");
const address = document.getElementById("address");
const password = document.getElementById("password");
const passwordConfirm = document.getElementById("con_password");
const signBtn = document.getElementById("sign_btn"); /// button
const verifyBtn = document.getElementById("verifyBtn"); /// button
const errorElement = document.querySelector(".error");
let customer_data = undefined;
const modal = document.getElementById("codeModel"); /// variafacation code modal
const parElement = modal.querySelector(".modal-content p");
const changeEmailElement = document.querySelector(".modal-content a"); /// button

/// sign up click handller
const signUpClickHandler = () => {
  customer_data = {
    first_name: firstName.value,
    last_name: lastName.value,
    email: email.value,
    phone: phone.value,
    address: address.value,
    password: password.value,
  };
  const customer = { ...customer_data };
  customer.password_confirm = passwordConfirm.value;

  const validation = isValidateUSerInput(customer);
  const errorMessage = buildValidationErrorMessage(validation);

  if (errorMessage) {
    console.log(errorMessage);
    // input field error element
    displayErrorAtElement(errorElement, errorMessage);
    return;
  }
  // if inputs is valid
  displayErrorAtElement(errorElement, "");

  /// send email to back end to generate otp
  fetchRequest("customer_email", "POST", { email: customer_data.email.trim() })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.status);
      }
      return response.json();
    })
    .then((json_data) => {
      if (json_data.status_code === 200) {
        console.log("success");
        showOTPModal(modal, parElement, customer_data.email);
      }
    })
    .catch((error) => console.log(error));
}; // end of method

signBtn.addEventListener("click", signUpClickHandler);

/////// change email handler
const changeEmailClickHandler = () => {
  hideModal(modal);
};
changeEmailElement.addEventListener("click", changeEmailClickHandler);

////// check code varifacation
const verifyClickHandler = () => {
  // get otp
  const otp = document.getElementById("emailCode").value;

  // validat code entered
  if (otp.trim().length === 0) {
    alert("enter OTP that sent to your email");
    return;
  }

  // if otp input not empty
  fetchRequest("customer_otp", "POST", {
    email: customer_data.email.trim(),
    otp: otp,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.status);
      }
      return response.json();
    })
    .then((json_data) => {
      console.log(json_data);
      if (json_data.status_code === 200) {
        console.log("success");
        // send customer data to backend      
        sendCustomer()
        window.location.href = "login.html";
      }
    })
    .catch((error) => {
      console.log("error is : " + error);
      if (error.message === "401") {
        displayErrorAtElement(
          document.getElementById("otpError"),
          "wrong code"
        );
      }
    });
};
verifyBtn.addEventListener("click", verifyClickHandler);

// send customer data to backend      
const sendCustomer = () => {
  console.log(customer_data)
  fetchRequest("customer", "POST", customer_data)
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.status);
      }
      return response.json();
    })
    .then( json_data =>{
      console.log(json_data)
      if(json_data.status_code === 200){
        console.log('success add')
      }
    }).catch( error => console.log(error))
};

