import { fetchRequest } from "./FetchRequest.js";
import { get_day , get_month, get_year} from "./DateTime.js";

// fetchRequest("customer_email", "POST", { email: "mdiaan442@gmail.com" }).then(
//   (response) => {
//       if (!response.ok){
//           throw new Error( response.status)
//       }
//     console.log(response.status)
//     return response.json()
//   }

// ).then(json_data =>{
//     console.log(json_data)
//     if (json_data.status_code === 409){
//         console.log('aleady signed')
//     }
// }).catch(error =>{
//     // console.log(error.message)
//     if (error.message === '409'){
//         console.log('aleady there')
//     }
// })

// document.cookie = "jwt=vhadkjhsk"

const getBtn = document.getElementById("getBtn");
const setBtn = document.getElementById("setBtn");

const getCookieHandler = () => {
  fetchRequest("get_cookie", "GET", undefined, true)
    .then((response) => {
      return response.json();
    })
    .then((json_data) => {
      console.log(json_data);
    })
    .catch((error) => console.log(error));
};

getBtn.addEventListener("click", getCookieHandler);


const setHandler = ()=>{
    fetchRequest("set_cookie", "GET", undefined, true)
  .then((response) => {
      console.log(response)
    return response.json();
  })
  .then((json_body) => {
    console.log(json_body);
  })
  .catch((error) => console.log(error));

}

setBtn.addEventListener('click', setHandler)





console.log(get_day())
console.log(get_month())
console.log(get_year())
