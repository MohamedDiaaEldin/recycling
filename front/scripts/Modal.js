


export const showOTPModal = (modal , parElement, email) => {
    parElement.textContent = "Enter code sent to  " + email;
  modal.style.display = "block";
};
export const showConfirmPrice = (modal , parElement, price) => {
    parElement.textContent = "Total price is " + price;
    modal.style.display = "block";
};

export const hideModal = (modal) => {
  modal.style.display = "none";
};
