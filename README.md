# Project_1
Client Query Management System: Organizing, Tracking, and Closing Support Queries

Project Description:

The Client Query Management System is a web application that allows clients to submit support queries and enables support teams to manage and resolve those queries efficiently.
The application is built using Python, Streamlit, and MySQL.

A CSV file is used only once to load historical queries into the database. After that, all new queries are handled in real time through the Streamlit interface.

Objectives:

1) Allow clients to submit queries online

2) Help support teams track and close queries

3) Measure query resolution time

4) Monitor open and closed queries

5) Improve support efficiency and customer satisfaction

How the System Works: 
CSV File (Historical Data)
        ↓
MySQL Database 
        ↓
Streamlit Web Application


CSV data is loaded into MySQL only once

MySQL becomes the main data source

Streamlit is used for user interaction

User Roles: 
Client

1) Register and log in

2) Submit a new query

3) Query status is automatically set to Open

4) Query creation time is generated automatically

Support:

1) Log in to the support dashboard

2) View all client queries

3) Filter queries by status and category

4) Close queries

5) View resolution time and performance metrics

Database Structure: 
Users Table:

1) Stores login details

2) Passwords are stored securely using hashing

Queries Table: 

1) Stores client queries

2) Tracks:

Query status (Open / Closed)

Query creation time

Query closure time

CSV Data Usage : 

CSV file is used only for initial data loading

CSV contains only date values

Time values are automatically added by Python

Random realistic times are assigned for better analysis

CSV is not used after database initialization

Key Features : 

1) Secure login system

2) Real-time query submission

3) Live support dashboard

4) nQuery status updates

5) Automatic time tracking

6) Resolution time calculation

7) Simple and interactive UI

Technologies Used : 

1) Python 3.14

2) Streamlit

3) MySQL 8.0

4) mysql-connector-python

5) pandas

6) bcrypt

7) DateTime

Project Files
Client_Query_Mangement_System
│
├── db_config.py        # Database connection and CSV loading
├── authentication.py  # Login and password handling
├── users.py            # Initial user creation (run once)
├── webapp.py           # Streamlit application
├── queriesdata.csv         # Historical query data
├── README.md           # Project documentation

How to Run the Project?: 
Step 1: Install Required Libraries
pip install streamlit pandas mysql-connector-python bcrypt

Step 2: Create MySQL Database

Run the provided SQL script to create tables and users.

Step 3: Insert Initial Users (One-Time)
python users.py

Step 4: Run the Application
python -m streamlit run webapp.py

Business Use Cases Covered : 

Client query submission

Query tracking and management

Support performance monitoring

Resolution time analysis

Workload identification

Conclusion :

This project demonstrates how a real-time query management system can be built using Python, MySQL, and Streamlit. It provides a clear separation between historical data and real-time operations while ensuring secure authentication and efficient query handling.

Thank you! 
