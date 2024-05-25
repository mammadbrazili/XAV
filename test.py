import streamlit as st
import pandas as pd
import dropbox
from io import BytesIO

# Dropbox access token
DROPBOX_ACCESS_TOKEN = 'sl.B16tSaMVJuMY81sQs6E0Ey5c28ko1Bd0fSVJPrZ2RlLDBCiIE9nHwWDXPtlivnVRWO-2W8vTbwRN9WUSCh-UsZcpo925K9q9nLtlyiSI4fMZkPLVU9njyl9pCG4qoKPInybF8COQet-I09zrCNs2KDk'

# Function to download the Excel file from Dropbox
def download_excel_from_dropbox(file_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    metadata, res = dbx.files_download(path=file_path)
    return BytesIO(res.content)

# Function to load the data into a DataFrame
def load_data(file_path):
    excel_file = download_excel_from_dropbox(file_path)
    df = pd.read_excel(excel_file)
    return df

# Streamlit app
def main():
    st.title("Dropbox Excel Data Dashboard")

    # Path to your Excel file in Dropbox
    dropbox_file_path = '/XAV coffee works/XAV Revenue/Excels/1403/بهار 1403/03 - خرداد/سفارشات کالا خرداد 1403.xlsx'

    # Load data
    data = load_data(dropbox_file_path)

    # Display data
    st.write("Data from Excel file:")
    st.dataframe(data)
    
if __name__ == "__main__":
    main()