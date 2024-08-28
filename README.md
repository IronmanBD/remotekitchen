# Remote Kitchen Backend 

An assessment task for managing restaurants, menus, and orders. It supports role-based access control, allowing owners, employees, and customers to interact with the system according to their permissions.

## Features

- **User Authentication**: JWT-based authentication.
- **Role-Based Access Control**: Owners, employees, and customers have different permissions.
- **Restaurant Management**: Owners can manage restaurants and their employees.
- **Menu Management**: Create and manage menus and items.
- **Order Processing**: Customers can place orders and make payments via Stripe.
- **Payment Integration**: Integrated with Stripe for payment processing.

## Technologies

- **Django**: Web framework.
- **Django Rest Framework**: API toolkit for Django.
- **PostgreSQL**: Database.
- **Stripe API**: Payment processing.
- **JWT**: JSON Web Token for authentication.

## Installation

```bash
git clone "https://github.com/IronmanBD/remotekitchen"
cd remotekitchen
python -m venv venv
pip install - r requirements.txt
python manage.py migrate
```
Setting up .env file with Stripe Keys.

### Authentication
- **POST** `/accounts/register/`  
  Register a new user.

- **POST** `/accounts/login/`  
  Log in and obtain a JWT.

- **POST** `/accounts/token/refresh/`  
  Refresh Token.

- **POST** `/accounts/logout/`  
  Logout User.

### Restaurants
- **GET** `/api/restaurants/`  
  List all restaurants.

- **POST** `/api/restaurants/`  
  Create a new restaurant (Owners only).

- **GET** `/api/restaurants/{id}/`  
  Retrieve a specific restaurant.

- **PUT** `/api/restaurants/{id}/`  
  Update a restaurant (Owners only).

- **DELETE** `/api/restaurants/{id}/`  
  Delete a restaurant (Owners only).

### Menus
- **GET** `/api/restaurants/menus/`  
  List all menus.

- **POST** `/api/restaurants/menus/`  
  Create a new menu (Owners).

- **GET** `/api/restaurants/{restaurant_id}/menus/{id}/`  
  Retrieve a specific menu.

- **PUT** `/api/restaurants/{restaurant_id}/menus/{id}/`  
  Update a menu (Owners).

- **DELETE** `/api/restaurants/{restaurant_id}/menus/{id}/`  
  Delete a menu (Owners).

- **GET** `/api/restaurants/{restaurant_id}/menus/{id}/items/`  
  Retrieve a specific menu.

- **POST** `/api/restaurants/menus/menus/{id}/items/`  
  Create a new menu (Owners).

- **GET** `/api/restaurants/{restaurant_id}/menus/{id}/items/{id}`  
  Retrieve a specific =id.

- **PUT** `/api/restaurants/{restaurant_id}/menus/{id}/items/{id}`  
  Update a id (Owners/Employees).

- **DELETE** `/api/restaurants/{restaurant_id}/menus/{id}/items/{id}`  
  Delete a id (Owners/Employees).

### Orders
- **GET** `/api/orders/`  
  List all orders.

- **POST** `/api/orders/`  
  Create a new order (Customers).

- **GET** `/api/orders/{id}/`  
  Retrieve a specific order.

- **PUT** `/api/orders/{id}/`  
  Update an order.

- **DELETE** `/api/orders/{id}/`  
  Cancel an order.

### Payments
- **POST** `/api/payments/`  
  Process a payment (Customers).
