const firstName = document.getElementById("first_name");
const lastName = document.getElementById("last_name");
const email = document.getElementById("email");
const phone = document.getElementById("phone");
const address = document.getElementById("address");
const password = document.getElementById("password");
const passwordConfirm = document.getElementById("con_password");
const signBtn = document.getElementById("sign_btn");
const verifyBtn = document.getElementById("verifyBtn");

/// variafacation code modal
const modal = document.getElementById("codeModel");

// is not empty
// password length
// password confirmation
// phone validation
function isValidateUSerInput(customer) {
  const errorMessage = {};
  errorMessage.empty = [];
  errorMessage.emptyValidation = false;
  errorMessage.passwordLength = true;
  errorMessage.passwordConfirmation = true;

  for (const input in customer) {
    if (customer[input].trim().length === 0) {
      errorMessage.empty.push(input);
      errorMessage.emptyValidation = true;
    }
  }

  // if field not empty
  if (errorMessage.emptyValidation === false) {
    // password length
    if (customer.password.trim().length < 8) {
      errorMessage.passwordLength = false;
    } else if (customer.password.trim() !== customer.password_confirm.trim()) {
      errorMessage.passwordConfirmation = false;
    }
  }
  return errorMessage;
}

const buildEmptyFields = (emptyFields) => {
  let formattedEmpty = "";
  for (field of emptyFields) {
    formattedEmpty += field + " \n";
  }
  return formattedEmpty;
};

const addCustomer = () => {
  customer = {
    firstName: firstName.value,
    lastName: lastName.value,
    email: email.value,
    phone: phone.value,
    address: address.value,
    password: password.value,
    password_confirm: passwordConfirm.value,
  };
  const validation = isValidateUSerInput(customer);
  let errorMessage = "error : ";
  let error = true;
  if (validation.emptyValidation) {
    errorMessage += "empty fields \n" + buildEmptyFields(validation.empty);
  } else if (validation.passwordLength === false) {
    errorMessage += "the password length must be at least 8 characters";
  } else if (validation.passwordConfirmation === false) {
    errorMessage += "the password confirmation doesn't match";
  } else {
    error = false; // there no error
  }
  const errorElement = document.querySelector(".error");
  if (error) {
    console.log(errorMessage);
    errorElement.textContent = errorMessage;
  } else {
    errorElement.textContent = "";

    fetch("http://localhost:5000/customer_email", {
      method: "POST",
      dataType: "json",
      mode: "cors",
      body: JSON.stringify({ email: customer.email.trim() }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.status_code === 200) {
          console.log("success");
          displayEmailPOp(customer.email);
        }
      })
      .catch((error) => console.log(error));
  }
};

signBtn.addEventListener("click", addCustomer);

const displayEmailPOp = (email) => {
  const parElement = modal.querySelector(".modal-content p");
  parElement.textContent = "Enter code sent to  " + email;
  modal.style.display = "block";
};

// change email handler
const changeEmailElement = document.querySelector(".modal-content a");

const changeEmailHandler = () => {
  modal.style.display = "none";
};

changeEmailElement.addEventListener("click", changeEmailHandler);
/// handel faild response
const updateOtpUi = () => {
  /// get error html tag
  otpErrorElement = document.getElementById("otpError");
  print(otpErrorElement);
  /// update ui
  otpErrorElement.textContent = "wrong code";
};

/// check code varifacation
const verifyClickHandler = () => {
  // get otp
  const otp = document.getElementById("emailCode").value;

  // validat code entered
  if (otp.trim().length === 0) {
    alert("enter OTP that sent to your email");
  } else {
    // make reuqets to validate otp

    fetch("http://localhost:5000/customer_otp", {
      method: "POST",
      dataType: "json",
      mode: "cors",
      body: JSON.stringify({ email: customer.email.trim(), otp: otp.trim() }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then(function (response) {
        if (!response.ok) {          
          throw new Error(response.status);
        }
        return response.json();
      })
      .then((data) => {
        // valid otp        
        if (data.status_code === 200) {          
          console.log("success");                

          /// TODO - send customer data to backend

          // go to login page           
          window.location.href = "login.html"          

        }
      })
      .catch((error) => {
        console.log("error is : " + error);        
        if (error.message === "401") {
          updateOtpUi()
        };
      });
    // make request with this code
    // get response
    // if valid code
    //    jump into login page
    // else
    ///   alert with error message
  }
};
verifyBtn.addEventListener("click", verifyClickHandler);
