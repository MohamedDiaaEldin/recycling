import { fetchRequest } from "./FetchRequest.js";

const new_sellBtn = document.getElementById("new_sell_orderBtn");
const logoutBtn = document.getElementById("logoutBtn");
const homeBtn = document.getElementById("home");
const activeBtn = document.getElementById("activeBtn");
const allBtn = document.getElementById("allBtn");
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

const clear_credentials = () => {
  window.localStorage.jwt = "";
  window.localStorage.public_id = "";
};

const display_orders = (all_order_data, active = false) => {
  // display points
  const total_pointsP = document.getElementById("total_points");
  total_pointsP.textContent = ` you have  ${all_order_data.total_points} points`;

  // display order data
  for (const order of all_order_data.orders) {
    if (active) {
      if (order.done === false) {
        display_order(order);
      }      
    } else {
      display_order(order);
    }
  }
};

const display_order = (order) => {
  /// if order.done === fasle
  /// add it to active

  //// add it to all

  const div = document.createElement("div");
  const pDate = document.createElement("p");
  const pTime = document.createElement("p");
  const pPoints = document.createElement("p");
  const pDetials = document.createElement("p");
  const pWeight = document.createElement("p");

  div.classList.add("order_info");
  div.classList.add("top_margin");
  div.classList.add("order_child");

  pDate.innerText = order.date;
  pTime.innerText = order.time;
  pPoints.innerText = order.points;
  pDetials.innerText = order.order_detials;
  pWeight.innerText = order.weight;

  div.appendChild(pDate);
  div.appendChild(pTime);
  div.appendChild(pPoints);
  div.appendChild(pDetials);
  div.appendChild(pWeight);

  const orderInfo = document.querySelector(".orders");
  orderInfo.appendChild(div);
};

const fetch_seller_data = (data) => {
  fetchRequest("sell_orders", "POST", data, false)
    .then((resposne) => {
      if (!resposne.ok) {
        throw new Error(resposne.status);
      }
      return resposne.json();
    })
    .then((json_data) => {
      if (json_data.status_code === 200) {
        // save all orders in local storage
        // localStorage.sell_orders = json_data;        
        localStorage.sell_orders = JSON.stringify(json_data);        
        activeBtn.click()
      }
    })
    .catch((error) => {
      if (error.message === "401") {
        // // clear local storage
        clear_credentials();
        console.log(error.message);
        window.location.href = "login.html";
      } else {
        console.log(error);
      }
    });
};

//   handel orders state
const jwt = window.localStorage.jwt;
const public_id = window.localStorage.public_id;
if (jwt === "" || public_id === "") {
  window.location.href = "login.html";
}

const data = { jwt: jwt, public_id: public_id };
if (seller_state) {
  fetch_seller_data(data);
  console.log("jwt and seller ");
} else {
  // TODO
  console.log("jwt and buyer ");
  // getJwt_data(jwt, 'buyer')
  // if not valid jwt:
  //       go to login page
  /// display data
}

const logoutClickHandler = () => {
  clear_credentials();
  window.location.href = "index.html";
};

const homeClickHandler = () => {
  window.location.href = "index.html";
};

logoutBtn.addEventListener("click", logoutClickHandler);
homeBtn.addEventListener("click", homeClickHandler);

new_sellBtn.addEventListener("click", () => {
  window.location.href = "new_sell.html";
});



const remove_orders_children = ()=>{
  for (const elemen of document.querySelectorAll('.order_child')){
    elemen.remove()
  }
}
activeBtn.addEventListener('click', ()=>{
  remove_orders_children()
    display_orders(JSON.parse(localStorage.sell_orders), true)
})
allBtn.addEventListener('click', ()=>{
  remove_orders_children()
  display_orders(JSON.parse(localStorage.sell_orders), false)
})