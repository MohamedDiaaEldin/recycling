const loginBtn = document.getElementById('loginBtn')
const email = document.getElementById('email')
const password = document.getElementById('password')

function isValidateUSerInput(customr){
    const errorMessage  = {}
    errorMessage.empty = false
    errorMessage.emptyFields = []

    for(const key in customr){
        if (customr[key].trim().length === 0){
            errorMessage.empty = true
            errorMessage.emptyFields.push(key)
        }
    }
    return errorMessage
}

/// build formatted empty field
const buildEmptyFields = (emptyFields)=>{
    let formattedEmpty = ""
    for(field of emptyFields){
      formattedEmpty += field +" \n"
    }
    return formattedEmpty
  }

const addCustomer = ()=>{
    
    customer = {        
        email: email.value,  
        password:password.value        
    } 
    
    const validation = isValidateUSerInput(customer)
    const errorElement = document.querySelector('.error')
    if(validation.empty){
        const errorMessage = "error: empty fields \n" + buildEmptyFields(validation.emptyFields) 
        errorElement.textContent = errorMessage
        // alert(errorMessage)
    }
    else{
        errorElement.textContent = ""

        // send reuest with data to validate user 
        // if valid :
        //      get jwt and save it 
        // else :
        //      not valid user data
    }   

    //   fetch("http://localhost:5000/login", {
    //     method: "POST",
    //     dataType: "json",
    //     mode: "cors",
    //     body: JSON.stringify(customer),
    //     headers: {
    //       "Content-Type": "application/json",
    //       Accept: "application/json",
    //     },
    //   })
    //     .then((r) => {
    //       // console.dir(r)
    //       return r.json();
    //     })
    //     .then((data) => {
    //       console.log(data);
    //       if (data.status_code === 200) {
    //         window.location.href = "success_login.html";
    //       } else if (data.status_code == 401) {
    //         alert("wrong email or password");
    //       } else {
    //         alert("email or password not correct");
    //       }
    //     })
    //     .catch((err) => console.log(err));    
}

loginBtn.addEventListener('click', addCustomer)