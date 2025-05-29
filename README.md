# Electronics Trading Platform

## Overview
This project is an **Electronics Trading Platform** built using **Python** and **Django REST Framework**. It provides APIs for managing users, employee statuses, products, sales network cells, and authentication using JWT tokens.

---

### Prerequisites
Python: Ensure Python 3.8+ is installed.

Django: Install Django and Django REST Framework.

Database: Configure a PostgreSQL database (or SQLite for development).

Environment Variables: Set up environment variables for database credentials and JWT secret keys.

### Setup Commands
Clone the Repository:


git clone https://github.com/Lampa97/electronics_trading_platform.git

cd electronics_trading_platform

#### Install Dependencies:

pip install -r requirements.txt

#### Apply Migrations:

python manage.py migrate

#### Run the Development Server:

python manage.py runserver

#### Create a Superuser:
python manage.py createadmin (using command from users application)

## Applications

### `users` Application
- Manages user accounts, employee statuses, and authentication.
- Provides endpoints for user creation, employee status updates, listing users, and obtaining JWT tokens.

### `api` Application
- Manages contacts, products, and sales network cells.
- Provides endpoints for CRUD operations on these entities.

---

## Models

### `users` Application Models
- **User**: Represents a user in the system. Includes fields like `email`, `password`, `is_active`, and `is_employee`.
  - New users are inactive by default and can only access all features after an admin changes their status to employees.

### `api` Application Models
- **Contact**: Represents a contact associated with sales network cells.
- **Product**: Represents products managed in the system.
- **SalesNetworkCell**: Represents hierarchical sales network cells with fields like `name`, `hierarchy_name`, `hierarchy_level`, `debt`, and `supplier`.
  - **Hierarchy Levels**:
    - `Factory`: Level 0
    - `Retail Network`: Level 1
    - `Individual Entrepreneur`: Level 2
  - **Debt Field**: The `debt` field can only be updated in the admin panel.

---

## API Routes

### `users` Application Routes
| **Route**                     | **Method** | **Description**                              | **Permissions** |
|--------------------------------|------------|----------------------------------------------|-----------------|
| `/users/register/`             | `POST`     | Create a new user account.                   | Public          |
| `/users/employee_status_update/` | `POST`     | Update employee status by `user_id` or `email`. | Admin Only          |
| `/users/list/`                 | `GET`      | List all users.                              | Admin Only      |
| `/users/employees/`            | `GET`      | List all employees.                          | Admin Only      |
| `/users/token/`                | `POST`     | Obtain JWT token.                            | Public          |

### `api` Application Routes
| **Route**          | **Method** | **Description**                                       | **Permissions** |
|--------------------|------------|-------------------------------------------------------|-----------------|
| `/contact/`        | `GET`      | List all contacts.                                    | Admin/Employee      |
| `/contact/<id>/`   | `GET`      | Retrieve a specific contact.                          | Admin/Employee       |
| `/contact/<id>/update/` | `PATCH`    | Update a specific contact.                            | Admin/Employee       |
| `/contact/<id>/destroy/` | `DELETE`   | Delete a specific contact.                            | Admin/Employee       |
| `/product/`        | `GET`      | List all products.                                    | Admin/Employee       |
| `/product/create/` | `POST`     | Create a new product.                                 | Admin/Employee       |
| `/product/<id>/`   | `GET`      | Retrieve a specific product.                          | Admin/Employee       |
| `/product/<id>/update/` | `PATCH`    | Update a specific product.                            | Admin/Employee       |
| `/product/<id>/destroy/` | `DELETE`   | Delete a specific product.                            | Admin/Employee       |
| `/cell/`           | `GET`      | List all sales network cells.                         | Admin/Employee       |
 | `/cell/?country=<country>` | `GET`      | Filter sales network cells by country (from Contact). | Admin/Employee  |
 | `/cell/create/`    | `POST`     | Create a new sales network cell.                      | Admin/Employee       |
| `/cell/<id>/`      | `GET`      | Retrieve a specific sales network cell.               | Admin/Employee       |
| `/cell/<id>/update/` | `PATCH`    | Update a specific sales network cell.                 | Admin/Employee       |
| `/cell/<id>/destroy/` | `DELETE`   | Delete a specific sales network cell.                 | Admin/Employee      |

---

## Tests

### Test Coverage
The project includes comprehensive tests for:
- **Users**: User creation, employee status updates, JWT token generation.
- **Contacts**: CRUD operations.
- **Products**: CRUD operations.
- **Sales Network Cells**: CRUD operations, hierarchy validation, and field updates.

### Running Tests
To run the tests, use the following command:
```bash
python manage.py test
```


## Notes
1. Admin/Employee permissions are required for most API operations.
2. New users can access all features only after their status is updated to employees by an admin.
3. The debt field in sales network cells can only be updated in the admin panel.