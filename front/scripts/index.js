// console.log(document.querySelector('h1').textContent)


const home = document.getElementById('home')
const orders = document.getElementById('orders')
const howItWorks = document.getElementById('howItWorks')
const aboutUs = document.getElementById('about')

let active = home

const homeHTML = document.getElementById('homeDEV')


const exchange =  (new_active)=>{
    active.style.color= "black"
    active = new_active
    active.style.color= "#02EC88"
}

const homeClickHandler = ()=> {    
    exchange(home)
    homeHTML.hidden = false
    
}
const ordersClickHandler = ()=> {  
    exchange(orders)
    homeHTML.hidden = true
}
const howItWorksClickHandler = ()=> {  
    exchange(howItWorks)
}

const aboutUsClickHandler = ()=> {  
    exchange(aboutUs)
}


home.addEventListener('click', homeClickHandler)
orders.addEventListener('click', ordersClickHandler)
howItWorks.addEventListener('click', howItWorksClickHandler)
aboutUs.addEventListener('click', aboutUsClickHandler)


// how it works

const buyer = document.getElementById('buyer')
const seller = document.getElementById('seller')
let selectedWorks = seller

const exchangeHowItWorks =  (new_selected)=>{
    selectedWorks.style.color= "black"
    selectedWorks = new_selected
    selectedWorks.style.color= "green"
}
exchangeHowItWorks(seller)

const buyerClickHandler = ()=>{
    exchangeHowItWorks(buyer)
    document.getElementById('buyer-div').hidden = true
}
buyer.addEventListener('click', buyerClickHandler)


const sellerClickHandler = ()=>{
    exchangeHowItWorks(seller)
    document.getElementById('buyer-div').hidden = false
}
seller.addEventListener('click', sellerClickHandler)


