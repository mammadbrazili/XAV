import streamlit as st
import pandas as pd
import streamlit as st
import random
import os 
import requests
import openpyxl
import altair as alt
import base64


# Using XAV Type Face

def load_black():
    font_file_path = "/Users/mohammad/Library/Fonts/xav black.ttf"
    with open(font_file_path, "rb") as font_file:
        font_data = font_file.read()
    encoded_font = base64.b64encode(font_data).decode("utf-8")
    css = f"@font-face {{ font-family: 'xav black'; src: url('data:application/octet-stream;base64,{encoded_font}'); }}"
    st.write('<style>{}</style>'.format(css), unsafe_allow_html=True)

def load_bold():
    font_file_path = "/Users/mohammad/Library/Fonts/xav semibold.ttf"
    with open(font_file_path, "rb") as font_file:
        font_data = font_file.read()
    encoded_font = base64.b64encode(font_data).decode("utf-8")
    css = f"@font-face {{ font-family: 'xav semibold'; src: url('data:application/octet-stream;base64,{encoded_font}'); }}"
    st.write('<style>{}</style>'.format(css), unsafe_allow_html=True)

def dropbox_download(link,string):
    # Modify the link to allow direct access
    direct_link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")

    # Use requests to get the content of the file
    response = requests.get(direct_link)

    # Check if the request was successful
    if response.status_code == 200:
        # Specify the local file name where the file will be saved
        local_filename = f"{string}.xlsx"  # Replace with your desired file name and extension
        
        # Save the content to a file
        with open(local_filename, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved as {local_filename}")
    else:
        print(f"Failed to retrieve the file. Status code: {response.status_code}")



# Function to read and concatenate excel files
def read_excel_files():
    df1 = pd.concat(pd.read_excel("ordibehesht.xlsx",sheet_name=None),ignore_index=True)
    df2 = pd.concat(pd.read_excel("khordad.xlsx",sheet_name=None),ignore_index=True)
    df = pd.concat([df1, df2], ignore_index=True)
    return df

# Function to clean the dataframe
def clean_dataframe(df):
    df["ردیف"] = df["ردیف"].fillna(method="ffill")
    df.dropna(subset=["نام محصول"], inplace=True)
    df = df.set_index("ردیف").reset_index()
    for i in df.index.to_list()[:-1]:
        row = df.loc[i, "ردیف"]
        next_row = df.loc[i+1, "ردیف"]
        if next_row == row:
            df.loc[i+1, ["تاریخ سفارش", "نام", "نام خانوادگی", "نام کافه", "شهر", "کد پیگیری"]] = df.loc[i, ["تاریخ سفارش", "نام", "نام خانوادگی", "نام کافه", "شهر", "کد پیگیری"]]
    return df

# Function to convert date
def convert_date(string):
    splited = string.split(" ")
    day = splited[-3]
    month_string = splited[-2]
    month = {"فروردین": 1, "اردیبهشت": 2, "خرداد": 3, "تیر": 4, "مرداد": 5, "شهریور": 6, "مهر": 7, "آبان": 8, "آذر": 9, "دی": 10, "بهمن": 11, "اسفند": 12}[month_string]
    year = splited[-1]
    return f"{year}/{month}/{day}"

# Function to generate date list based on user input
def generate_date_list(start, end):
    start_day, start_month, year = int(start.split("/")[-1]), int(start.split("/")[-2]), int(start.split("/")[0])
    end_day, end_month = int(end.split("/")[-1]), int(end.split("/")[-2])
    date_list = []
    if start_day <= end_day:
        for i in range(start_day, end_day + 1):
            date_list.append(f"{year}/{start_month}/{i}")
    else:
        for i in range(start_day, 32):
            date_list.append(f"{year}/{start_month}/{i}")
        for i in range(1, end_day + 1):
            date_list.append(f"{year}/{end_month}/{i}")
    return date_list

# Function to clean the dataframe based on date list
def filter_and_clean_dataframe(df, date_list):
    span_df = df[df["تاریخ سفارش"].isin(date_list)]
    rows_to_delete = [i for i in span_df.index.to_list() if str(span_df.loc[i, "کد پیگیری"])[:4] in ["هدیه", "مصرف"] or str(span_df.loc[i, "نام"])[:4] in ["هدیه", "مصرف"]]
    gifts_df = span_df.loc[rows_to_delete]
    span_df = span_df.drop(rows_to_delete)
    return span_df

# Function to plot data using Streamlit
def plot_data(data_dict, title):
    data = pd.DataFrame(list(data_dict.items()), columns=["دسته", "مقدار"])
    # Randomize colors for bars from a list of nude colors
    nude_colors = ['#f3e5ab', '#d7c4bb', '#f1c5b3', '#e0a899', '#c0b283', '#f5e4b3', '#f6d9d1', '#c8c2be']
    data['Color'] = [random.choice(nude_colors) for _ in range(len(data))]
    
    # Create the bar chart using Altair
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('دسته', sort=None, axis=alt.Axis(labelAngle=-45)),
        y='مقدار',
        color=alt.Color('Color', scale=None)
    ).properties(
        title=title
    )

    # Add text labels for each bar
    text = chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-10  # Adjust this value to move the text higher or lower
    ).encode(
        text='مقدار'
    )
    
    # Combine the chart and text
    final_chart = chart + text
    
    # Display the chart in Streamlit
    st.altair_chart(final_chart, use_container_width=True)

# Streamlit app
def main():
    load_black()
    load_bold()
    dropbox_download("https://www.dropbox.com/scl/fi/d1wux79gl92h9narou4xf/1403.xlsx?rlkey=sh5cljzhvpx2qcrhmln34vtwj&st=sk2kb5s2&dl=0", "ordibehesht")
    dropbox_download("https://www.dropbox.com/scl/fi/dlrfovoroyljqdketdcl9/1403.xlsx?rlkey=rk8p65pggu839rpupq39lz99z&st=kenx4ebp&dl=0", "khordad")


    st.markdown("<h1 style='text-align: center; font-family: xav black;'>گزارش فروش دپارتمان درآمد</h3>", unsafe_allow_html=True)

    # User inputs for start and end date
    st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'> تاریخ شروع گزارش (فرمت برای مثال ۱۴۰۳/۲/۵)</div>", unsafe_allow_html=True)
    start_date = st.text_input("")
    st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'> تاریخ شروع گزارش (فرمت برای مثال ۱۴۰۳/۳/۵)</div>", unsafe_allow_html=True)
    end_date = st.text_input(" ")

    if start_date and end_date:
        df = read_excel_files()
        df = clean_dataframe(df)
        df.dropna(subset=["تاریخ سفارش", "تعداد"], inplace=True)
        df["تاریخ سفارش"] = df["تاریخ سفارش"].apply(convert_date)
        for i in df.index.to_list():
            try:
                count = int(df.loc[i, "تعداد"])
                df.loc[i, "واحد فرعی"] = df.loc[i, "واحد فرعی"] * count
            except:
                continue
        date_list = generate_date_list(start_date, end_date)
        span_df = filter_and_clean_dataframe(df, date_list)

        # Whole sale
        total_sale = sum(span_df["واحد فرعی"].to_list()) / 1000

        # Each Line Sale
        span_df["نام محصول"] = span_df["نام محصول"].apply(lambda x: x.split("|")[-1])
        v_dict, a_dict, x_dict = {}, {}, {}
        for i in list(span_df["نام محصول"].value_counts().keys()):
            a = span_df[span_df["نام محصول"] == i]
            kg = round(sum(a["واحد فرعی"].to_list()) / 1000, 3)
            code = str(span_df[span_df["نام محصول"] == i]["کد محصول"].to_list()[0])[0]
            if code == "5":
                v_dict[i] = kg
            elif code == "3":
                a_dict[i] = kg
            elif code == "1":
                x_dict[i] = kg

        # Each Cafe Buy
        cafe_list = set(span_df["نام کافه"].to_list())
        cafe_dict = {i: round(sum(span_df[span_df["نام کافه"] == i]["واحد فرعی"].to_list()) / 1000, 3) for i in cafe_list}
        top_cafe = sorted(cafe_dict, key=lambda k: cafe_dict[k], reverse=True)[:11]
        top_cafe_dict = {i: cafe_dict[i] for i in top_cafe}

        # Each City Buy
        city_list = set(span_df["شهر"].to_list())
        city_dict = {i: round(sum(span_df[span_df["شهر"] == i]["واحد فرعی"].to_list()) / 1000, 3) for i in city_list}
        top_city = sorted(city_dict, key=lambda k: city_dict[k], reverse=True)[:11]
        top_city_dict = {i: city_dict[i] for i in top_city}

        # Plotting Total sale based on the series
        v_series_sale = sum(v_dict.values())
        a_series_sale = sum(a_dict.values())
        x_series_sale = sum(x_dict.values())
        plot_dict = {"X Series": x_series_sale, "A Series": a_series_sale, "V Series": v_series_sale, "Total": total_sale}

        # Displaying plots
        plot_data(plot_dict, "فروش به تفکیک سری")
        plot_data(v_dict, "V فروش سری")
        plot_data(a_dict, "A فروش سری")
        plot_data(x_dict, "X فروش سری")
        plot_data(top_cafe_dict, " فروش ۱۰ کافه اول")
        plot_data(top_city_dict, "فروش ۱۰ شهر اول")
    

if __name__ == "__main__":
    main()
