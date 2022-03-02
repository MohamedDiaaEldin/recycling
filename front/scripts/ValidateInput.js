


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

    errorMessage.empty = getEmptyFields(customer)
    if (errorMessage.empty.length > 0){        
        errorMessage.emptyValidation = true;
    }
    
    // second validation phase
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




export const getEmptyFields = obj =>{
  const emptyFields = []
  for (const input in obj) {
    if (obj[input].trim().length === 0) {
      emptyFields.push(input)    
    }
  }
  return emptyFields 
}



/// for login 
export  function isValidLoginInput(customr){
  const errorMessage  = {}
  errorMessage.empty = false
  errorMessage.emptyFields = []


  errorMessage.emptyFields = getEmptyFields(customr)
  if ( errorMessage.emptyFields.length > 0){
      errorMessage.empty = true
  }

  return errorMessage
}


