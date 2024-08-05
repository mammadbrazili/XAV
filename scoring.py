import os
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def authorize_gspread(credentials_file):
    creds = None
    token_file = "token.json"
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    
    return creds

def run_sheet():
    credentials_file = "/Users/mohammad/Sepita/credentials.json"  # Update this path to your credentials file
    creds = authorize_gspread(credentials_file)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1fzCF_K8eKmKJwgcLpfQw9VVBsTdU-gL63fIEC3OxcUw").sheet1
    return sheet

def write_to_sheet(sheet, values):
    row_count = len(sheet.get_all_values())
    sheet.insert_row(values, row_count + 1)
    st.success(f"Data inserted into row {row_count + 1}")

def read_sheet(sheet):
    values = sheet.get_all_values()
    if not values:
        st.warning("No data found in the sheet.")
        return pd.DataFrame()
    
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def get_inputs():
    name = st.text_input("نام ")
    last_name = st.text_input("نام خانوادگی")
    phone = st.text_input("شماره تماس ")
    date = st.text_input("تاریخ سفارش ")
    
    # List of 30 options for the 'service' dropdown
    service_options = ["پیراهن", "شلوار", "کت", "کت و شلوار", "پیراهن زنانه", "پیراهن مجلسی", "لباس رنگی", "تیشرت",
                       "لباس زیر", "تاپ", "مانتو", "روسری و شال", "کفش و کتانی", "کیف", "کوله‌پشتی", "پتو", "ملحفه",
                         "روتختی", "پرده", "روفرشی", "کوسن", "متکا", "چادر","چادر ماشین", "خیاطی"]
    selected_options = st.multiselect("Select multiple options:", service_options)

    selected_data = []

    # Display input widgets for each selected option to get the count and price
    if selected_options:
        for option in selected_options:
            count = st.number_input(f"Enter count for {option}:", min_value=0, value=1, step=1, key=f"{option}_count")
            price = st.number_input(f"Enter price for {option}:", min_value=0.0, value=0.0, step=0.01, format="%.2f", key=f"{option}_price")
            selected_data.append({"service": option, "count": count, "price": price})

    bargain = st.text_input("تخفیف ")
    payment_status = st.text_input("وضعیت پرداخت ")
    order_notes = st.text_input("توضیحات مشتری ")
    
    return name, last_name, phone, date, selected_data, bargain, payment_status, order_notes

def get_next_order_id(df):
    if df.empty:
        return 100
    else:
        return df["شماره سفارش"].astype(int).max() + 1

def main():
    st.title("Data Entry and Display with Google Sheets")
    # activate sheet
    sheet = run_sheet()
    df = read_sheet(sheet)
    
    # activate variables
    name, last_name, phone, date, selected_data, bargain, payment_status, order_notes = get_inputs()

    # Get the next order ID
    order_id = get_next_order_id(df)

    # Prepare new rows to be added
    new_rows = []
    for data in selected_data:
        new_row = [order_id, name, last_name, phone, date, data['service'], data['count'], data['price'], bargain, payment_status, order_notes]
        new_rows.append(new_row)
    
    # Convert new rows to DataFrame
    new_df = pd.DataFrame(new_rows, columns=["شماره سفارش", "نام", "نام خانوادگی", "شماره تماس", "تاریخ سفارش", "خدمت", "تعداد", "قیمت", "تخفیف", "وضعیت پرداخت", "توضیحات مشتری"])
    
    # Append new rows to the existing DataFrame
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Display current data in the sheet
    st.header("Current Data")
    st.write(df)
    
    # Write new rows to the Google Sheet
    for new_row in new_rows:
        write_to_sheet(sheet, new_row)

if __name__ == "__main__":
    main()
