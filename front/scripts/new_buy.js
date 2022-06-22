import { fetchRequest } from "./FetchRequest.js";
import { hideModal, showConfirmPrice } from "./Modal.js";

const error_p = document.getElementById('error')
const categoriesSelect = document.getElementById("categories");
const matrialsSelect = document.getElementById("matrials");
//inputs 
const dateInput = document.getElementById('date_input')
const timeInput = document.getElementById('time_input')
const weightInput = document.getElementById('weigth_input')
const modal = document.getElementById("codeModel")
const parElement = modal.querySelector(".modal-content p");
// buttons
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");
const confirmBtn = document.getElementById('confirmBtn')
const cancel_price = document.querySelector('.verify a')


const addCategory = (item, selected) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.name;
    /// add category to selected
    selected.appendChild(option);
};

const addCategories = (selectedItems, selected) => {
    for (const category of selectedItems) {
        addCategory(category, selected);
    }
};

/// main script
// fetch and display categories
fetchRequest("categories", "GET", undefined, false)
    .then((response) => {
        if (!response.ok) {
            throw new Error(response.status);
        }
        return response.json();
    })
    .then((json_data) => {
        if (json_data.status_code === 200) {
            addCategories(json_data.categories, categoriesSelect);
        }
    })
    .catch((error) => {
        console.log(error);
    });

// fetch and display matrials
fetchRequest("matrials", "GET", undefined, false)
    .then((response) => {
        if (!response.ok) {
            throw new Error(response.status);
        }
        return response.json();
    })
    .then((json_data) => {
        if (json_data.status_code === 200) {
            addCategories(json_data.matrials, matrialsSelect);
        }
    })
    .catch((error) => {
        console.log(error);
    });

const get_selected = (selected) => {
    return selected.options[selected.selectedIndex]
}



const buy_order_handler = () => {
    const data = {
        "jwt": localStorage.jwt,
        "public_id": localStorage.public_id,
        "date": dateInput.value,
        "time": timeInput.value,
        "category_id": parseInt(categoriesSelect.options[categoriesSelect.selectedIndex].value),
        "matrial_id": parseInt(matrialsSelect.options[matrialsSelect.selectedIndex].value),
        "weight": parseInt(weightInput.value)
    }
    fetchRequest('buy_order', 'POST', data, false).then(response => {
        if (!response.ok) {
            throw new Error(response.status)
        }
        return response.json()
    }).then(json_data=>{
        if(json_data.status_code === 200){
            window.location.href = "orders.html"
        }

    }).catch(error => {
        if (error.message === '401') {
            localStorage.jwt = ""
            localStorage.public_id = ""
            window.location.href = 'index.html'
        }else if(error.message === '404'){
            error_p.textContent = "weight is not available try another weight"
        }
       
    })
}

/// get form data   
/// validate input data TODO
// send data to the back end  with jwt and public_id 
const submitClickHandler = () => {
    console.log(weightInput)
    const data = {
        "jwt": localStorage.jwt,
        "public_id": localStorage.public_id,
        "category_id": parseInt(categoriesSelect.options[categoriesSelect.selectedIndex].value),
        "matrial_id": parseInt(matrialsSelect.options[matrialsSelect.selectedIndex].value),
        "weight": parseInt(weightInput.value)
    }

    fetchRequest('confirm_buy', 'POST', data, false).then(response => {
        if (!response.ok) {
            throw new Error(response.status)
        }
        return response.json()
    }).then(json_data => {
        if (json_data.status_code === 200) {
            // response with 200 will have data not fount or confirm 
            if (json_data.message) {
                error_p.textContent = "weight is not available try another weight"
            }
            else {
                error_p.textContent = ""
                showConfirmPrice(modal, parElement, json_data.price)

            }
        }

    }).catch(error => {
        if (error.message === '401') {
            localStorage.jwt = ""
            localStorage.public_id = ""
            window.location.href = 'index.html'
        }
    })

};

submitBtn.addEventListener("click", submitClickHandler);


cancelBtn.addEventListener('click', () => {
    window.location.href = 'orders.html'
})


cancel_price.addEventListener('click', () => {
    hideModal(modal)
})

confirmBtn.addEventListener('click', buy_order_handler)