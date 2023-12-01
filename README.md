# Bikya - Material Waste Management Application

Bikya is a web application designed to address the issue of material waste. It allows customers to select material types, specify weights, dates, times, and locations for waste collection. Additionally, the admin panel enables viewing all placed orders and tracking deliveries associated with each order.



## Introduction

Bikya aims to streamline waste collection by providing a platform where users can schedule and manage waste pickup conveniently.

## Features
### App Demo
https://github.com/MohamedDiaaEldin/recycling/assets/72948823/a921549b-3a8a-4948-8bd3-64dfbe6a4779

### Check it out
[mdiaa.pythonanywhere.com/](https://mdiaa.pythonanywhere.com/static/index.html)

- **User Portal:**
  - Select material type for disposal.
  - Specify weight, date, time, and location for waste collection.

- **Admin Panel:**
  - View all orders made by customers.
  - Track ongoing deliveries associated with each order.

- **Delivery Panel:**
  - Daily orders for each delivery personnel.
  - Confirm orders by visiting customers , weighing the material and confirm the order via the web application.

- **Customer Notifications:**
  - Upon successful order confirmation, customers receive an email notification about the order status and earned reward points.



## Tech Stack

### Backend

- **Python:** Core programming language for server-side logic.
- **Flask:** Web framework used for building the backend application.
- **SQLAlchemy:** Python SQL toolkit and Object-Relational Mapping (ORM) used for database management.
- **PyJWT:** Python implementation of JSON Web Tokens (JWT) for user authentication.
- **PostgreSQL:** Relational database management system utilized as the backend database.

### Frontend

- **HTML, CSS, JavaScript:** Essential technologies for building the user interface and handling client-side functionalities.

## Installation

### Backend Setup

1. **Clone the repository:**
   ```bash
   cd bikya-backend
2. Install dependencies:
   ```bash 
   pip install -r requirements.txt
3. Configure the PostgreSQL database.
4. Run The Flask application.
    ```bash
    ./run.sh
