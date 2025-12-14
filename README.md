# Week 7: Secure Authentication System

Student Name: Rudy Munda  
Student ID: M01028388  
Course: CST1510 – CW2 – Multi-Domain Intelligence Platform

## Project Description

A command-line authentication system implementing secure password hashing.  
This system allows users to register accounts and log in with proper password verification.

## Features

- Secure password hashing using bcrypt with automatic salt generation  
- User registration with duplicate username prevention  
- User login with password verification  
- Input validation for usernames and passwords  
- File-based user data persistence  

## Technical Implementation

- Hashing Algorithm: bcrypt with automatic salting  
- Data Storage: Plain text file (`users.txt`) with comma-separated values  
- Password Security: One-way hashing, no plaintext storage  
- Validation: Username (3–20 alphanumeric characters), Password (minimum 6 characters)

## Week 8: SQLite Database & CRUD Operations

Student Name: Rudy Munda
Student ID: M01028388
Course: CST1510 – CW2 – Multi-Domain Intelligence Platform

## Project Description

This week introduces the use of SQLite databases for building persistent data systems.
The project involves creating a database, defining tables, and implementing basic CRUD operations through Python.

## Features

Creation of an SQLite database

Definition of tables (users, incidents, datasets, tickets)

Inserting new records into tables

Updating and deleting existing records

Fetching and displaying data

File-based database storage (intelligence_platform.db)

## Technical Implementation

Database engine: SQLite

Python library: sqlite3

SQL operations: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE

Parameterized queries to avoid SQL injection

Connection and cursor management using Python

Ensuring tables are created only once using CREATE TABLE IF NOT EXISTS

## Week 9: Streamlit Dashboard & Multi-Page Interface

Student Name: Rudy Munda
Student ID: M01028388
Course: CST1510 – CW2 – Multi-Domain Intelligence Platform

## Project Description

This week focuses on creating a Streamlit web dashboard with a multi-page structure.
The goal is to display database content, create interactive components, and lay the foundation for an intelligence platform.

## Features

Streamlit multi-page application (Home.py + /pages folder)

Login interface using session state

Displaying database tables in the UI

Basic filters, charts, and widgets

Dynamic components such as forms and buttons

Real-time page updates using session state

## Technical Implementation

Framework: Streamlit

State Management: st.session_state

UI Components: tables, buttons, forms, inputs, sliders

Data source: SQLite database and CSV files

Modular file organisation for clean architecture

Routing using Streamlit’s built-in page system

## Week 10: AI Integration Using the OpenAI API

Student Name: Rudy Munda
Student ID: M01028388
Course: CST1510 – CW2 – Multi-Domain Intelligence Platform

## Project Description

This week introduces the integration of AI assistants into the Streamlit dashboard.
Students connect their app to the OpenAI API and build an in-page AI helper capable of answering user queries.

## Features

Importing and configuring the OpenAI client

Secure API key storage in .streamlit/secrets.toml

Custom AI assistant widget inside Streamlit

User prompt submission and AI-generated responses

Multi-domain support (Cyber, Data Science, IT)

Real-time AI feedback for the dashboard

## Technical Implementation

AI Model: GPT-4o-mini or equivalent

Python client: openai

API key loaded securely from st.secrets

Assistant function returning structured responses

Error handling for failed requests

Integration into every page via a reusable module (services/ai_widget.py) 


## RUNNING CODE EXPLANATION 

The application is run by navigating to the project folder using cd my_app and starting the Streamlit application with streamlit run Home.py, which launches the system locally and allows users to log in and access the different dashboards through a web interface.