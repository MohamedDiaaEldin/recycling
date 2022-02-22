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

const buyerBtn = document.getElementById('buyerBtn')
const sellerBtn = document.getElementById('sellerBtn')
const sellerTemplate = document.getElementById('sellerTemplate').content.cloneNode(true)
const buyerTemplate = document.getElementById('buyerTemplate').content.cloneNode(true)
const howItWorksSection = document.querySelector('.how-it-works')
let selectedWorks = sellerBtn

// set seller to be first displayed
let lastAdded = sellerTemplate
howItWorksSection.appendChild(document.getElementById('sellerTemplate').content.cloneNode(true))     

const exchangeColorHowItWorks =  (new_selected)=>{
    selectedWorks.style.color= "black"
    selectedWorks = new_selected
    selectedWorks.style.color= "green"
}


const sellerClickHandler= ()=>{
    exchangeColorHowItWorks(sellerBtn)        
    if (lastAdded == buyerTemplate){
        const added  = document.getElementById('buyer-how-it-works')
        howItWorksSection.removeChild(added)
        howItWorksSection.appendChild(document.getElementById('sellerTemplate').content.cloneNode(true))     
    }       

    window.scrollBy(0, 300);
    lastAdded = sellerTemplate
}
sellerBtn.addEventListener('click', sellerClickHandler)

sellerBtn.click()

const buyerClickHandler = ()=>{
    exchangeColorHowItWorks(buyerBtn)            
    if (lastAdded == sellerTemplate){
        const added  = document.getElementById('seller-how-it-works')                
        howItWorksSection.removeChild(added)        
        howItWorksSection.appendChild(document.getElementById('buyerTemplate').content.cloneNode(true))            
    }   

    lastAdded = buyerTemplate 
    window.scrollBy(0, 300);
}
buyerBtn.addEventListener('click', buyerClickHandler)
