/// sigun input validation
// is not empty
// password length
// password confirmation
// phone validation - not implement yet TODO
export function isValidateUSerInput(customer) {
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