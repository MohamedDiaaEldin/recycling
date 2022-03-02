
/// display error message at html element
export const displayErrorAtElement = (element, err_message)=>{
    element.textContent = err_message
}


export const buildEmptyFields = (emptyFields) => {
  let formattedEmpty = "";
  for (const field of emptyFields) {
    formattedEmpty += field + " \n";
  }
  return formattedEmpty;
};

// recives validate objects which contains information about sigun up input validation 
export const buildValidationErrorMessage = (validation)=>{

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
  if (error){
      return errorMessage
  }
  return ''
}  


