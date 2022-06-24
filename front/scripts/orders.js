import { fetchRequest } from "./FetchRequest.js";

const new_sellBtn = document.getElementById("new_sell_orderBtn");
const logoutBtn = document.getElementById("logoutBtn");
const homeBtn = document.getElementById("home");
const activeBtn = document.getElementById("activeBtn");
const allBtn = document.getElementById("allBtn");
const switch_btn = document.getElementById("switchBtn");
const total_points = document.getElementById('total_points')
const price_point = document.getElementById('price_point')
const jwt = window.localStorage.jwt;
const public_id = window.localStorage.public_id;



const display_sell_orders = (all_order_data, active = false) => {
  // display points
  const total_pointsP = document.getElementById("total_points");
  console.log(  all_order_data.total_points)
  total_pointsP.textContent = ` you have  ${all_order_data.total_points} points`;

  // display order data
  for (const order of all_order_data.orders) {
    if (active) {
      if (order.done === false) {
        display_sell_order(order);
      }
    } else {
      display_sell_order(order);
    }
  }
};


const display_buy_orders = (all_order_data, active = false) => { 
  // display order data
  for (const order of all_order_data.orders) {
    if (active) {
      if (order.done === false) {
        display_buy_order(order);
      }
    } else {
      display_buy_order(order);
    }
  }
};



const display_sell_order = (order) => {
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

const display_buy_order = (order) => {
  /// if order.done === fasle
  /// add it to active

  //// add it to all

  const div = document.createElement("div");
  const pDate = document.createElement("p");
  const pTime = document.createElement("p");
  const priceP = document.createElement("p");
  const pDetials = document.createElement("p");
  const pWeight = document.createElement("p");

  div.classList.add("order_info");
  div.classList.add("top_margin");
  div.classList.add("order_child");

  pDate.innerText = order.date;
  pTime.innerText = order.time;
  priceP.innerText = order.price;
  pDetials.innerText = order.order_detials;
  pWeight.innerText = order.weight;

  div.appendChild(pDate);
  div.appendChild(pTime);
  div.appendChild(priceP);
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


const fetch_buyer_data = (data) => {
  fetchRequest("buy_orders", "POST", data, false)
    .then((resposne) => {
      if (!resposne.ok) {
        throw new Error(resposne.status);
      }
      return resposne.json();
    })
    .then((json_data) => {
      if (json_data.status_code === 200) {
        // save all buy  orders in local storage
        localStorage.buy_orders = JSON.stringify(json_data);
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


const logoutClickHandler = () => {
  clear_credentials();
  window.location.href = "index.html";
};

const homeClickHandler = () => {
  window.location.href = "index.html";
};

logoutBtn.addEventListener("click", logoutClickHandler);
homeBtn.addEventListener("click", homeClickHandler);


const remove_orders_children = () => {
  for (const elemen of document.querySelectorAll('.order_child')) {
    elemen.remove()
  }
}

const clear_credentials = () => {
  window.localStorage.jwt = "";
  window.localStorage.public_id = "";
};

///////////////////////////////

const change_buyer_ui = () => {
  new_sellBtn.textContent = 'new buy order'
  switch_btn.textContent = 'switch to seller'
  total_points.style.display = 'none'
  price_point.textContent = 'price'

}
const change_seller_ui = () => {
  new_sellBtn.textContent = 'new sell order'
  switch_btn.textContent = 'switch to buyer'
  total_points.style.display = 'block'
  price_point.textContent = 'points'
}

const handel_seller = () => {
  change_seller_ui()

  new_sellBtn.addEventListener('click', () => {
    window.location.href = "new_sell.html"
  })

  activeBtn.addEventListener('click', () => {
    remove_orders_children()
    display_sell_orders(JSON.parse(localStorage.sell_orders), true)
  })

  allBtn.addEventListener('click', () => {
    remove_orders_children()
    display_sell_orders(JSON.parse(localStorage.sell_orders), false)
  })
  
}
const handel_buyer = () => {
  change_buyer_ui()
  new_sellBtn.addEventListener('click', () => {
    window.location.href = "new_buy.html"
  })
  activeBtn.addEventListener('click', () => {
    remove_orders_children()
    display_buy_orders(JSON.parse(localStorage.buy_orders), true)
  })
  allBtn.addEventListener('click', () => {
    remove_orders_children()
    display_buy_orders(JSON.parse(localStorage.buy_orders), false)
  })
}

switch_btn.addEventListener('click', () => {

  const type = typeof localStorage.seller_state
  console.log('type is ', type)
  if (type === typeof (undefined) || localStorage.seller_state === 'true') {
    localStorage.seller_state = false
    window.location.href = "orders.html"
  }
  else{
    localStorage.seller_state = true
    window.location.href = "orders.html"
  }

})

if (jwt === "" || public_id === "") {
  window.location.href = "login.html";
}
const data = { jwt: jwt, public_id: public_id }


// handel buyer and seller state

const type = typeof localStorage.seller_state
console.log('type is ', type)
  
if (type === typeof (undefined) || localStorage.seller_state === 'true') {
  handel_seller()
  fetch_seller_data(data)
}
else {
  handel_buyer()
  // fetch buyer data
  fetch_buyer_data(data)
}
