import { fetchRequest } from "./FetchRequest.js";
import { getEmptyFields } from "./ValidateInput.js";
import { buildEmptyFields } from "./HandelErrors.js";
import { isValidLoginInput } from "./ValidateInput.js";
import { displayErrorAtElement } from "./HandelErrors.js";

const loginBtn = document.getElementById("loginBtn");
const email = document.getElementById("email");
const password = document.getElementById("password");
const signupBtn = document.getElementById("signupBtn");

/// user input validation
const loginClickHandler = () => {
  const customer = {
    email: email.value,
    password: password.value,
  };

  const validation = isValidLoginInput(customer);

  const errorElement = document.querySelector(".error");
  /// If there is empty fields
  if (validation.empty) {
    const errorMessage =
      "error: empty fields \n" + buildEmptyFields(validation.emptyFields);
    displayErrorAtElement(errorElement, errorMessage);
    return;
  }
  /// esle 
  /// make request with login data
  displayErrorAtElement(errorElement, "");

  fetchRequest("login", "POST", customer)
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.status);
      }
      return response.json();
    })
    .then((json_data) => {
      if (json_data.status_code === 200) {
          // TODO
          // recive jwt and store it as cookie  
          /// go to order page 
        alert("logined in :)");
      }
    })
    .catch((error) => {
        // if user unauthorized
      if (error.message === "401")
        displayErrorAtElement(errorElement, "wrong email or password");
    });
};
loginBtn.addEventListener("click", loginClickHandler);

// sign up click listner
signupBtn.addEventListener("click", () => {
  document.location.href = "signup.html";
});
