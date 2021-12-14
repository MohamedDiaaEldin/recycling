const loginBtn = document.getElementById('loginBtn')
const email = document.getElementById('email')
const password = document.getElementById('password')

// loginBtn.addEventListener('click', getUser)
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
        email: email.value,  
        password:password.value        
      } 
    if (! isValidateUSerInput(customer)){
          alert('check your inputs')
          return
    }

    console.log(customer)
      fetch('http://localhost:5000/login', {
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
            console.log(data)
            if (data.status_code === 200 ){                
                window.location.href = "success_login.html";            
            }
            else if ( data.status_code == 401){
                alert('wrong email or password')
            }
            else{
                alert('email or password not correct')
            }
        })
        .catch(err => console.log(err))    
}

loginBtn.addEventListener('click', addCustomer)