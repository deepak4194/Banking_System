# Banking System

This project, titled "Banking System," is a simple, interactive application for managing fundamental banking operations, such as account creation, secure logins, balance checks, deposits, and withdrawals. The application is designed using Python, Streamlit, and SQLite, offering a user-friendly interface and robust data security features. It serves as a basic banking system suited for educational and small-scale use cases.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Database Schema](#database-schema)
5. [Setup Instructions](#setup-instructions)
6. [Usage](#usage)
7. [Future Enhancements](#future-enhancements)

## Introduction
The Banking System project provides a secure and efficient solution for basic banking operations. It is designed with an emphasis on simplicity, data security, and ease of use. By using SQLite for the backend and Streamlit for the front-end interface, this project ensures seamless interaction for users and protects sensitive account information.

## Features
- **Account Creation**: Allows users to create a new bank account with unique account numbers.
- **Login System**: Secure login using account number and password.
- **Balance Inquiry**: Users can check their current account balance after logging in.
- **Deposit Funds**: Enables users to deposit money into their accounts.
- **Withdraw Funds**: Allows users to withdraw money, ensuring that the balance does not go below zero.
- **Logout**: Clears session data to protect sensitive information after logging out.

## Requirements
- **Hardware Requirements**
  - Standard computer/server
  - 1 GHz processor, 4 GB RAM recommended
  - 100 MB storage space

- **Software Requirements**
  - Python 3.x
  - Streamlit
  - SQLite3
  - Additional Python Libraries: `streamlit`, `sqlite3`, `random`

## Database Schema
The database consists of a single table `Bank` with the following columns:
- **account_name** (`TEXT`): Full name of the account holder.
- **acc_no** (`INTEGER PRIMARY KEY`): Unique account number.
- **password** (`TEXT`): User password for secure login.
- **balance** (`INTEGER`): Current balance of the account.

## Setup Instructions
1. Clone the repository.
2. Install the required libraries:
   ```bash
   pip install streamlit sqlite3
