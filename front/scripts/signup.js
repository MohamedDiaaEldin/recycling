const user_email = document.getElementById('email')
const firstName = document.getElementById('first_name')
const lastName = document.getElementById('last_name')
const password = document.getElementById('password')
const address = document.getElementById('address')
const signBtn = document.getElementById('signBtn')


function isValidateUSerInput(customr){
    for(const key in customr){
        if (customr[key].length === 0){
            return false
        }
    }
    return true
}
const addCustomer = ()=>{
    
    customer = {
        name: firstName.value + " " + lastName.value,
        email: email.value,  
        password:password.value,
        address:address.value,  
      } 
      if (! isValidateUSerInput(customer)){
          alert('check your inputs')
          return
      }
    // console.log(customer)
      fetch('http://localhost:5000/customer', {
        method: 'POST',  
        dataType: 'json',
        mode:'cors',
        body:JSON.stringify(customer),  
        headers : { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
      }    
      })
        .then(r => {
            // console.dir(r)          
            return r.json()
          })
        .then(data => {                                              
            if (data.status_code === 200 ){
                console.log('yes')
                window.location.href = "success_signup.html";            
            }            
        })
        .catch(err => console.log(err))    
}

signBtn.addEventListener('click', addCustomer)
