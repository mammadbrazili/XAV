import os
import pandas as pd
import streamlit as st
from datetime import datetime
from persiantools.jdatetime import JalaliDate


# Function to read Excel file
def read_excel(file_path):
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        st.warning(f"{file_path} does not exist. Creating a new file.")
        return pd.DataFrame()

# Function to write to Excel file
def write_to_excel(file_path, df):
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

# Function to get the next order ID
def get_next_order_id(df):
    if df.empty:
        return 100
    else:
        return df["شماره سفارش"].astype(int).max() + 1

# Function to get user inputs for the Order page
def get_inputs():
    name = st.text_input("نام ")
    last_name = st.text_input("نام خانوادگی")
    phone = st.text_input("شماره تماس ")
    date = st.text_input("تاریخ سفارش ")

    # List of 30 options for the 'service' dropdown
    service_options = ["پیراهن", "شلوار", "کت", "کت و شلوار", "پیراهن زنانه", "پیراهن مجلسی", "لباس رنگی", "تیشرت",
                       "لباس زیر", "تاپ", "مانتو", "روسری و شال", "کفش و کتانی", "کیف", "کوله‌پشتی", "پتو", "ملحفه",
                       "روتختی", "پرده", "روفرشی", "کوسن", "متکا", "چادر", "چادر ماشین", "خیاطی"]
    selected_options = st.multiselect("انتخاب کنید:", service_options)

    selected_data = []

    # Display input widgets for each selected option to get the count, price, and checkboxes
    if selected_options:
        for option in selected_options:
            count = st.number_input(f"تعداد {option}:", min_value=1, value=1, step=1, key=f"{option}_count")
            price = st.number_input(f"قیمت {option}:", min_value=10000, value=10000, step=5000, key=f"{option}_price")
            
            # Add checkboxes for additional options
            clean = st.checkbox("شست و شو", key=f"{option}_clean")
            iron = st.checkbox("اتو", key=f"{option}_iron")
            color = st.checkbox("لکه‌گیری", key=f"{option}_color")
            
            selected_data.append({
                "service": option,
                "count": count,
                "price": price,
                "clean": clean,
                "iron": iron,
                "color": color
            })

    payment_status = st.text_input("وضعیت پرداخت ")
    order_notes = st.text_input("توضیحات مشتری ")
    
    return name, last_name, phone, date, selected_data, payment_status, order_notes

# Main function
def main():
    # Create a sidebar for page navigation
    page = st.sidebar.selectbox("Navigate", ["سفارش‌گیری", "تحویل", "دفتر هزینه"])

    if page == "سفارش‌گیری":
        st.title("خشک‌شویی سپیتا")

        # Define the Excel file path
        excel_file = "/Users/mohammad/Sepita/orders.xlsx"

        # Read the existing data from the Excel file
        df = read_excel(excel_file)

        # Get user inputs
        name, last_name, phone, date, selected_data, payment_status, order_notes = get_inputs()

        # Add a submit button at the end
        if st.button("ثبت"):
            if name and last_name and phone and date and selected_data:
                # Get the next order ID
                order_id = get_next_order_id(df)

                # Prepare new rows to be added
                new_rows = []
                for data in selected_data:
                    new_row = [
                        order_id, name, last_name, phone, date, data['service'], data['count'],
                        data["clean"] ,  data['iron'],  data['color'],data["count"], 
                        data['price'] , ((data['price'] * data['count'])), payment_status, order_notes," "
                    ]
                    new_rows.append(new_row)

                # Convert new rows to DataFrame
                new_df = pd.DataFrame(new_rows, columns=[
                    "شماره سفارش", "نام", "نام خانوادگی", "شماره تماس", "تاریخ سفارش", "خدمت", "تعداد",  "شست و شو", "اتو", "لکه‌گیری","مانده", 
                    "هزینه واحد",'هزینه مجموع', "وضعیت پرداخت", "توضیحات مشتری", "تاریخ دریافت"
                ])

                # Append new rows to the existing DataFrame
                df = pd.concat([df, new_df], ignore_index=True)

                # Write the updated DataFrame back to the Excel file
                write_to_excel(excel_file, df)
                st.success("با موفقیت ذخیره شد.")
            else:
                st.warning("Please fill in all the required fields.")

        # Display current data in the Excel file
        st.header("لیست سفارش‌ها")
        st.write(df)

    elif page == "تحویل":
        # Define the Excel file path
        excel_file = "/Users/mohammad/Sepita/orders.xlsx"

        # Getting the order number
        order_no = st.number_input("شماره سفارش", min_value=0, value=0, step=1)

        # Read the existing data from the Excel file
        df = read_excel(excel_file)

        # Orders of customer
        df_customer = df[df["شماره سفارش"] == order_no]
        st.header("لیست سفارش‌")
        st.write(df_customer)

        # List to store checkbox labels
        checkbox_labels = df_customer["خدمت"].to_list()

        # Generate checkboxes dynamically with unique keys
        checkbox_states = {}
        for idx, label in enumerate(checkbox_labels):
            checkbox_states[label] = st.checkbox(label, key=f"checkbox_{idx}")

        # Manage actions based on checkbox states
        for idx, (label, state) in enumerate(checkbox_states.items()):
            # if user checked 
            if state:
                receive_date = st.text_input(f"تاریخ دریافت {label}", key=f"receive_date_{idx}")
                df.loc[(df['شماره سفارش'] == order_no) & (df["خدمت"] == label), "تاریخ دریافت"] = receive_date
                df.loc[(df['شماره سفارش'] == order_no) & (df["خدمت"] == label), "مانده"] = 0
                df.loc[(df['شماره سفارش'] == order_no) & (df["خدمت"] == label), "وضعیت پرداخت"] = "پرداخت شده"  
                st.write(df) 
    
    elif page == "دفتر هزینه":
        # Load Excel file or create if it doesn't exist
        def load_data(file_path):
            try:
                data = pd.read_excel(file_path)
            except FileNotFoundError:
                data = pd.DataFrame(columns=["Date", "Category", "Subcategory", "Description", "Amount"])
            return data

        # Save the data back to the Excel file
        def save_data(file_path, data):
            with pd.ExcelWriter(file_path, engine="openpyxl", mode='a' if 'Sheet1' in pd.ExcelFile(file_path).sheet_names else 'w') as writer:
                data.to_excel(writer, index=False)

        # Define categories and subcategories
        categories = {
            "Fixed Costs": ["Rent/Lease", "Utilities", "Salaries", "Insurance", "Depreciation", "Loan Repayments"],
            "Variable Costs": ["Laundry Supplies", "Repairs and Maintenance", "Utility Bills", "Employee Wages (Variable)", "Packaging Materials", "Transportation Costs"],
            "Marketing and Advertising": ["Online Marketing", "Local Advertising"],
            "Miscellaneous Costs": ["Software and IT", "Licenses and Permits", "Waste Disposal", "Professional Services", "Security"],
            "Unexpected Costs": ["Emergency Repairs", "Price Fluctuations"],
            "Inventory Management": ["Inventory Costs", "Losses/Theft"]
        }

        # User Interface
        st.title("Laundry Business Expense Tracker")

        # Handle session state for category selection
        if 'category' not in st.session_state:
            st.session_state['category'] = list(categories.keys())[0]

        # Input form for adding expenses
        with st.form("expense_form"):
            persian_date_input = st.text_input("Date (YYYY-MM-DD in Persian calendar)", value=str(JalaliDate.today()))
            
            # Select category with session state tracking
            category = st.selectbox("Category", list(categories.keys()), index=list(categories.keys()).index(st.session_state['category']))
            st.session_state['category'] = category  # Update the session state

            # Dynamically update subcategories based on selected category
            subcategory = st.selectbox("Subcategory", categories[st.session_state['category']])
            
            description = st.text_input("Description")
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            submitted = st.form_submit_button("Add Expense")

        # Convert Persian date to Gregorian date
        try:
            gregorian_date = JalaliDate(*map(int, persian_date_input.split('-'))).to_gregorian()
        except ValueError:
            st.error("Please enter a valid Persian date in YYYY-MM-DD format.")
            submitted = False

        # Load existing data
        file_path = "/Users/mohammad/Sepita/expenses.xlsx"
        data = load_data(file_path)

        # Add new expense
        if submitted:
            new_expense = {
                "Date": gregorian_date,
                "Category": category,
                "Subcategory": subcategory,
                "Description": description,
                "Amount": amount
            }
            data = data.append(new_expense, ignore_index=True)
            save_data(file_path, data)
            st.success("Expense added successfully!")

        # Display stored expenses
        st.subheader("Stored Expenses")
        st.dataframe(data)
if __name__ == "__main__":
    main()   
