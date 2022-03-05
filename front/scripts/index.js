// console.log(document.querySelector('h1').textContent)

const home = document.getElementById("home");
const orders = document.getElementById("orders");
const howItWorks = document.getElementById("howItWorks");
const aboutUs = document.getElementById("about");
const logBtn = document.getElementById("loginBtn"); // or logout

let activeMenueElement = home;
const homeHTML = document.getElementById("homfunePage");

const displayLogoutButton = () => {
  loginBtn.id = "logoutBtn";
  loginBtn.textContent = "logout";
  const logoutBtn = document.getElementById("logoutBtn");
  logoutBtn.addEventListener("click", () => {
    window.localStorage.jwt = "";
    logoutBtn.textContent = "login";
  });
};


/// TODO
/* function is_valid_jwt(jwt, public_id):{
  fetch to /verify
}
*/



//  handel login and logout state
jwt = window.localStorage.jwt;
if (jwt === "") {  // or not valid jwt  TODO
  // dsiplay login button
  logBtn.textContent = "login";
  logBtn.addEventListener("click", () => {
    window.location.href = "login.html";
  });
} else {
  // dsiplay logout button
  logBtn.textContent = "logout";
  logBtn.addEventListener("click", () => {    
    window.localStorage.jwt = ""
    window.localStorage.public_id = ""    
    /// back to login text
    logBtn.textContent = "login";
    logBtn.addEventListener("click", () => {
      window.location.href = "login.html";
    });
  });
}

const exchange = (new_active) => {
  activeMenueElement.style.color = "black";
  activeMenueElement = new_active;
  activeMenueElement.style.color = "#02EC88";
};

const homeClickHandler = () => {
  exchange(home);
};
const ordersClickHandler = () => {
  window.location.href = "orders.html";
};
const howItWorksClickHandler = () => {
  exchange(howItWorks);
};

const aboutUsClickHandler = () => {
  exchange(aboutUs);
};

home.addEventListener("click", homeClickHandler);
orders.addEventListener("click", ordersClickHandler);
howItWorks.addEventListener("click", howItWorksClickHandler);
aboutUs.addEventListener("click", aboutUsClickHandler);

// how it works
const buyerBtn = document.getElementById("buyerBtn");
const sellerBtn = document.getElementById("sellerBtn");
const sellerTemplate = document
  .getElementById("sellerTemplate")
  .content.cloneNode(true);
const buyerTemplate = document
  .getElementById("buyerTemplate")
  .content.cloneNode(true);
const howItWorksSection = document.querySelector(".how-it-works");
let selectedWorks = sellerBtn;

// set seller to be first displayed
let lastAdded = sellerTemplate;
howItWorksSection.appendChild(
  document.getElementById("sellerTemplate").content.cloneNode(true)
);

// change color buyer and seller colors
const exchangeColorHowItWorks = (new_selected) => {
  selectedWorks.style.color = "black";
  selectedWorks = new_selected;
  selectedWorks.style.color = "green";
};

//// handel seller click - how it works
const sellerClickHandler = () => {
  exchangeColorHowItWorks(sellerBtn);
  if (lastAdded == buyerTemplate) {
    const added = document.getElementById("buyer-how-it-works");
    howItWorksSection.removeChild(added);
    howItWorksSection.appendChild(
      document.getElementById("sellerTemplate").content.cloneNode(true)
    );
  }
  lastAdded = sellerTemplate;
};
sellerBtn.addEventListener("click", sellerClickHandler);

sellerBtn.click();

//// handel buyer click - how it works
const buyerClickHandler = () => {
  exchangeColorHowItWorks(buyerBtn);
  if (lastAdded == sellerTemplate) {
    const added = document.getElementById("seller-how-it-works");
    howItWorksSection.removeChild(added);
    howItWorksSection.appendChild(
      document.getElementById("buyerTemplate").content.cloneNode(true)
    );
  }

  lastAdded = buyerTemplate;
};
buyerBtn.addEventListener("click", buyerClickHandler);
