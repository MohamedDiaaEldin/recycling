// import {fetchRequest} from 'FetchRequest.js'

const new_sellBtn = document.getElementById("new_sell_orderBtn");
const logoutBtn = document.getElementById("logoutBtn");
const homeBtn = document.getElementById("home");

const seller_state = true;
/*
          <div class="order_info">
            <p>15 / 1</p>
            <p>3:30</p>
            <p>10</p>
            <p>plastic-bottle</p>
            <p>2.5</p>
          </div>
*/

const getOrder_data = (jwt, public_id, flag) => {
  data = { jwt: jwt, public_id: public_id };
  if (flag === "seller") {
    // fetch seller
    // TODO
  } else {
      // TODO
    // fetch buyer
  }
};

//
const jwt = window.localStorage.jwt;
if (jwt === "") {
  window.location.href = "login.html";
}
/// there is jwt and seller is online
else if (seller_state) {
    // TODO
  // getJwt_data(jwt, 'seller')
  // if not valid jwt:
  //       go to login page
  // display it
  console.log("jwt and seller ");
}
/// there is jwt and buyer is online
else {
    // TODO
  console.log("jwt and buyer ");
  // getJwt_data(jwt, 'buyer')
  // if not valid jwt:
  //       go to login page
  /// display data
}

const logoutClickHandler = () => {
  window.localStorage.jwt = "";
  window.location.href = "index.html";
};

const homeClickHandler = () => {
  window.location.href = "index.html";
};

logoutBtn.addEventListener("click", logoutClickHandler);
homeBtn.addEventListener("click", homeClickHandler);

/* 
function getData(jwt , flag) 
    /// fetch end point to get orders and points data 
    /// if valid jwt : 
    ///     return extracted data 
    /// else :
    //      return empty

*/

// if there  jwt
// data  = getData(jwt , 'seller')
// if data is empty :
// go to login
// else :
/// display data

/// click handler for switch to buyer
// data  = getData(jwt , 'buyer')
// if data is empty :
// go to login
// else :
/// display data

////////
// const newSellClickHandler = () => {
//   const div = document.createElement("div");
//   const pDate = document.createElement("p");
//   const pTime = document.createElement("p");
//   const pPoints = document.createElement("p");
//   const pDetials = document.createElement("p");
//   const pWeight = document.createElement("p");

//   div.classList.add("order_info");

//   pDate.innerText = "15/1";
//   pTime.innerText = "15/1";
//   pPoints.innerText = "15/1";
//   pDetials.innerText = "15/1";
//   pWeight.innerText = "15/1";

//   div.appendChild(pDate);
//   div.appendChild(pTime);
//   div.appendChild(pPoints);
//   div.appendChild(pDetials);
//   div.appendChild(pWeight);

//   const orderInfo = document.querySelector(".orders_data");
//   console.log(orderInfo);
//   orderInfo.appendChild(div);
// };
// new_sellBtn.addEventListener("click", newSellClickHandler);
