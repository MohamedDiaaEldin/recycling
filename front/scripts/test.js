import { fetchRequest } from "./FetchRequest.js";


fetchRequest("customer_email", "POST", { email: "mdiaan442@gmail.com" }).then(
  (response) => {
      if (!response.ok){
          throw new Error( response.status)
      }
    console.log(response.status)    
    return response.json()
  }

).then(json_data =>{
    console.log(json_data)
    if (json_data.status_code === 409){
        console.log('aleady signed')
    }
}).catch(error =>{    
    // console.log(error.message)
    if (error.message === '409'){
        console.log('aleady there')
    }   
})
