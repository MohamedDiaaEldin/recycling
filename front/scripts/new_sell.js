import { fetchRequest } from "./FetchRequest.js";

const categoriesSelect = document.getElementById("categories");
const matrialsSelect = document.getElementById("matrials");
const zonesSelect = document.getElementById("zones");
//inputs 
const dateInput = document.getElementById('date_input')
const timeInput = document.getElementById('time_input')
const weightInput = document.getElementById('weigth_input')

// buttons
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");

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


  const addZone = (item, selected) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.name;
    /// add zone to selected
    selected.appendChild(option);
};
const addZones = (selectedItems, selected) => {
    for (const zone of selectedItems) {
        addZone(zone, selected);
    }
};

const get_selected = (selected)=>{
    return selected.options[selected.selectedIndex]
}




/// get form data   
/// validate input data TODO
// send data to the back end  with jwt and public_id 
const submitClickHandler = () => {    
    console.log(weightInput)
    const sell_order_data = {
        "category_id" : categoriesSelect.options[categoriesSelect.selectedIndex].value, 
        "matrial_id" : matrialsSelect.options[matrialsSelect.selectedIndex].value,
        "zone_id" : zonesSelect.options[zonesSelect.selectedIndex].value,
        "date" : dateInput.value,
        "time" : timeInput.value ,    
        "weight" : weightInput.value 
    }   
    const data = {
        "jwt" : localStorage.jwt,
        "public_id" : localStorage.public_id,
        "sell_data" : sell_order_data
    }
    print(data)

    fetchRequest('sell_order', 'POST', data, false).then( response =>{
        if (!response.ok){
            throw new Error(response.status)
        }
        return response.json()
    }).then( json_data =>{
        if ( json_data.status_code === 200){
            window.location.href = 'orders.html'
        }

    }).catch( error =>{
        if (error.message === '401'){
            localStorage.jwt = ""
            localStorage.public_id = ""
            window.location.href = 'index.html'
        }
    })

};
fetchRequest("zones", "GET", undefined, false)
    .then((response) => {
        if (!response.ok) {
            throw new Error(response.status);
        }
        return response.json();
    })
    .then((json_data) => {
        if (json_data.status_code === 200) {
            addZones(json_data.zones, zonesSelect);
        }
    })
    .catch((error) => {
        console.log(error);
    });

submitBtn.addEventListener("click", submitClickHandler);


cancelBtn.addEventListener('click', ()=>{
    window.location.href = 'orders.html'
})