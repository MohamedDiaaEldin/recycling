// console.log(document.querySelector('h1').textContent)


const home = document.getElementById('home')
const orders = document.getElementById('orders')
const howItWorks = document.getElementById('howItWorks')
const aboutUs = document.getElementById('about')
const loginBtn = document.getElementById('loginBtn')

let activeMenueElement = home
const homeHTML = document.getElementById('homePage')

const exchange =  (new_active)=>{
    activeMenueElement.style.color= "black"
    activeMenueElement = new_active
    activeMenueElement.style.color= "#02EC88"
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
const buyerBtn = document.getElementById('buyerBtn')
const sellerBtn = document.getElementById('sellerBtn')
const sellerTemplate = document.getElementById('sellerTemplate').content.cloneNode(true)
const buyerTemplate = document.getElementById('buyerTemplate').content.cloneNode(true)
const howItWorksSection = document.querySelector('.how-it-works')
let selectedWorks = sellerBtn

// set seller to be first displayed
let lastAdded = sellerTemplate
howItWorksSection.appendChild(document.getElementById('sellerTemplate').content.cloneNode(true))     

// change color buyer and seller colors
const exchangeColorHowItWorks =  (new_selected)=>{
    selectedWorks.style.color= "black"
    selectedWorks = new_selected
    selectedWorks.style.color= "green"
}

//// handel seller click - how it works
const sellerClickHandler= ()=>{
    exchangeColorHowItWorks(sellerBtn)        
    if (lastAdded == buyerTemplate){
        const added  = document.getElementById('buyer-how-it-works')
        howItWorksSection.removeChild(added)
        howItWorksSection.appendChild(document.getElementById('sellerTemplate').content.cloneNode(true))     
    }           
    lastAdded = sellerTemplate
}
sellerBtn.addEventListener('click', sellerClickHandler)

sellerBtn.click()

//// handel buyer click - how it works
const buyerClickHandler = ()=>{
    exchangeColorHowItWorks(buyerBtn)            
    if (lastAdded == sellerTemplate){
        const added  = document.getElementById('seller-how-it-works')                
        howItWorksSection.removeChild(added)        
        howItWorksSection.appendChild(document.getElementById('buyerTemplate').content.cloneNode(true))            
    }   

    lastAdded = buyerTemplate 
}
buyerBtn.addEventListener('click', buyerClickHandler)



//  handel login button 

const loginClickHandler = ()=>{
    window.location.href = "login.html"
}
loginBtn.addEventListener('click', loginClickHandler)