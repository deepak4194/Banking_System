import streamlit as st
import sqlite3
import random

# Custom CSS for styling with hover effect
st.markdown("""
    <style>
            
            /* Change the overall background color */
        body {
            background-color: blue;  /* Light blue-gray background color */
        }
        /* Main title styling */
        .title {
            color: #2c3e50;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
        }
        
        /* Sidebar title styling */
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
            color: #2c3e50;
        }
        
        /* Buttons styling with hover effect */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 16px;
            border: none;
            
        }
        
        /* Hover effect for buttons */
        .stButton>button:hover {
            background-color: #45a049;  /* Darker green shade on hover */
            color: white;
        }
        
        /* Center content on page */
        .main-content {
            max-width: 600px;
            margin: auto;
        }
        
        /* Text input field styling */
        .stTextInput>div>div>input {
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
        }
        
    </style>
""", unsafe_allow_html=True)

# Initialize database connection
def init_connection():
    conn = sqlite3.connect("Bank.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS Bank (
                    account_name TEXT,
                    acc_no INTEGER PRIMARY KEY,
                    password TEXT,
                    balance INTEGER)""")
    return conn

# Reset session state to clear previous login details
def reset_session():
    st.session_state["logged_in"] = False
    st.session_state["account_number"] = None
    st.session_state["balance"] = 0
    st.session_state["page"] = "home"

# Initialize session state variables
if "logged_in" not in st.session_state:
    reset_session()

# Main function
def main():
    st.title("Welcome to ABC Bank")
    conn = init_connection()
    c = conn.cursor()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Create Account", "Login", "Banking Operations"])

    if page == "Home":
        st.write("Select an option from the sidebar to get started.")
        st.session_state["page"] = "home"

    elif page == "Create Account":
        # Account Creation
        st.header("Create a New Account")
        first_name = st.text_input("Enter Your First Name").strip().upper()
        last_name = st.text_input("Enter Your Last Name").strip().upper()
        password = st.text_input("Set a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Create Account"):
            if first_name and last_name:
                if password == confirm_password:
                    name = f"{first_name} {last_name}"
                    acc_no = random.randint(10000000, 99999999)
                    c.execute("INSERT INTO Bank (account_name, acc_no, password, balance) VALUES (?, ?, ?, ?)", 
                              (name, acc_no, password, 0))
                    conn.commit()
                    st.success(f"Account created successfully for {name}. Your account number is {acc_no}.")
                    reset_session()  # Clear session after account creation
                else:
                    st.error("Passwords do not match.")
            else:
                st.error("Please enter valid names.")

    elif page == "Login":
        # Login Section
        st.header("Login to Your Account")
        account_number_input = st.text_input("Enter Your Account Number")
        password_input = st.text_input("Enter Your Password", type="password")
        
        if st.button("Login"):
            if account_number_input.isdigit():
                account_number = int(account_number_input)
                result = c.execute("SELECT * FROM Bank WHERE acc_no=? AND password=?", 
                                   (account_number, password_input)).fetchone()
                if result:
                    st.session_state["logged_in"] = True
                    st.session_state["account_number"] = account_number
                    st.session_state["balance"] = result[3]
                    st.success("Logged in successfully!")
                    st.session_state["page"] = "operations"
                else:
                    st.error("Invalid account number or password.")
            else:
                st.error("Please enter a valid account number.")

    elif page == "Banking Operations" and st.session_state["logged_in"]:
        # Banking Operations after Login
        st.header("Choose an Operation")
        operation = st.radio("Select an operation", ("Check Balance", "Deposit", "Withdraw"))

        # Check Balance
        if operation == "Check Balance":
            st.info(f"Your current balance is ₹{st.session_state['balance']}.")

        # Deposit
        elif operation == "Deposit":
            deposit_amount = st.number_input("Enter the amount to deposit", min_value=1)
            if st.button("Deposit"):
                new_balance = st.session_state["balance"] + deposit_amount
                c.execute("UPDATE Bank SET balance = ? WHERE acc_no = ?", (new_balance, st.session_state["account_number"]))
                conn.commit()
                st.session_state["balance"] = new_balance
                st.success(f"Deposited ₹{deposit_amount} successfully. New balance: ₹{st.session_state['balance']}.")

        # Withdraw
        elif operation == "Withdraw":
            withdraw_amount = st.number_input("Enter the amount to withdraw", min_value=1)
            if st.button("Withdraw"):
                if withdraw_amount <= st.session_state["balance"]:
                    new_balance = st.session_state["balance"] - withdraw_amount
                    c.execute("UPDATE Bank SET balance = ? WHERE acc_no = ?", (new_balance, st.session_state["account_number"]))
                    conn.commit()
                    st.session_state["balance"] = new_balance
                    st.success(f"Debited ₹{withdraw_amount} successfully. New balance: ₹{st.session_state['balance']}.")
                else:
                    st.error("Insufficient balance.")

        # Log Out
        if st.button("Log Out"):
            reset_session()
            st.success("Logged out successfully.")
            st.sidebar.radio("Go to", ["Home"], index=0)  # Redirect to home page

    else:
        st.warning("Please log in to access Banking Operations.")

    conn.close()

if __name__ == "__main__":
    main()
