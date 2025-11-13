# WealthWise Portfolio Tracker (Backend)

A **FastAPI-based backend system** for managing user stock portfolios — featuring secure authentication (JWT), stock transactions (BUY/SELL), and automatic portfolio summary with profit/loss calculations.

---

##  Project Overview

WealthWise helps users:
- Register and log in securely using JWT authentication  
- Record stock transactions (BUY and SELL)  
- View portfolio summary (holdings, average cost, total value, and gain/loss)

This backend is built using **Python, FastAPI, PostgreSQL, and SQLAlchemy ORM**.

---
## Folder Structure

![Folder Structure](screenshots/folder-structure.png)

---

##  Steps to Run the "WealthWise Portfolio Tracker" Backend

### 1. Setup Database
1. Open **PgAdmin**
2. Create a new database:
   ```sql
   CREATE DATABASE wealthnest;
   Import database structure and sample data from setup.sql

### 2. Setup Virtual Environment

python -m venv venv
venv\Scripts\activate       # (Windows)  

 OR

source venv/bin/activate    # (Mac/Linux)

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Environment Variables

DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/wealthnest

JWT_SECRET=your_secret_key

JWT_ALGORITHM=HS256

JWT_EXP_MINUTES=60


### 5. Run the FastAPI Server

uvicorn app.main:app --reload

### 6. Access the Application
Swagger Docs → http://127.0.0.1:8000/docs


## Developed Modules
 ### 1. Authentication (JWT Based)
/auth/register → Register new user

/auth/login → Login and generate JWT token

Click on authorize button and use the generated token  to authorize

 ### 2. Transactions
/transactions/current → Add new BUY/SELL transaction

/transactions → Fetch all user transactions

 ### 3. Portfolio
/portfolio/summary → Get holdings, total value, and profit/loss

 ### 4. Users
/users/current → see current logged-in user

/users → Fetch all users

---


##  Screenshots

###  Swagger UI
![Swagger Docs](screenshots/swagger-docs.png)

---

###  Database Tables

| Table | Screenshot |
|--------|-------------|
| Users Table | ![Users Table](screenshots/tables/users-table.png) |
| Transactions Table | ![Transactions Table](screenshots/tables/transactions-table.png) |
| Prices Table | ![Prices Table](screenshots/tables/prices-table.png) |

---

###  API Calls
| API Endpoint                            | Screenshots                                                                                                                    |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **POST `/auth/register`**               | ![](screenshots/API-calls/register-request.png)     ![](screenshots/API-calls/register-response.png) |
| **POST `/auth/login`**                  |  ![](screenshots/API-calls/login-request.png)     ![](screenshots/API-calls/login-response.png)       |
| **GET `/users/me`**                     | ![](screenshots/API-calls/current-user.png)                                                                                    |
| **GET `/users`**                        | ![](screenshots/API-calls/list-users.png)                                                                                      |
| **POST `/transactions/current` (BUY)**  | ![](screenshots/API-calls/add-buy-transaction.png)                                                                             |
| **POST `/transactions/current` (SELL)** | ![](screenshots/API-calls/add-sell-transaction.png)                                                                            |
| **GET `/transactions/`**       | ![](screenshots/API-calls/list-transactions-of-current-user.png)                                                               |
| **GET `/portfolio/summary`**            | ![](screenshots/API-calls/portfolio-summary.png)                                                                               |
| **Authorized User (JWT Token)**         | ![](screenshots/API-calls/authorized-user.png)                                                                                 |


---



 **Note:**  
All screenshots were taken from Swagger UI and PostgreSQL tables for the project.
