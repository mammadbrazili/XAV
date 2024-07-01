import streamlit as st
import pandas as pd
import streamlit as st
import random
import os 
import requests
import openpyxl
import altair as alt
import base64
from datetime import datetime, timedelta
from convertdate import persian
from io import BytesIO



# Using XAV Type Face

def load_black():
    font_file_path = "xav black.ttf"
    with open(font_file_path, "rb") as font_file:
        font_data = font_file.read()
    encoded_font = base64.b64encode(font_data).decode("utf-8")
    css = f"@font-face {{ font-family: 'xav black'; src: url('data:application/octet-stream;base64,{encoded_font}'); }}"
    st.write('<style>{}</style>'.format(css), unsafe_allow_html=True)

def load_bold():
    font_file_path = "xav semibold.ttf"
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
    df3 = pd.concat(pd.read_excel("farvardin.xlsx",sheet_name=None),ignore_index=True)
    df4 = pd.concat(pd.read_excel("tir.xlsx",sheet_name=None),ignore_index=True)
    

    df = pd.concat([df1, df2,df3,df4], ignore_index=True)
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

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=True, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


def persian_to_gregorian(year, month, day):
    return persian.to_gregorian(year, month, day)

def gregorian_to_persian(year, month, day):
    return persian.from_gregorian(year, month, day)

def generate_date_list(start, end):
    # Split the input dates
    start_year, start_month, start_day = map(int, start.split('/'))
    end_year, end_month, end_day = map(int, end.split('/'))

    # Convert Persian dates to Gregorian dates
    start_gregorian = persian_to_gregorian(start_year, start_month, start_day)
    end_gregorian = persian_to_gregorian(end_year, end_month, end_day)

    # Convert tuples to datetime objects
    start_date_gregorian = datetime(*start_gregorian)
    end_date_gregorian = datetime(*end_gregorian)

    # Generate date range
    date_list = []
    current_date = start_date_gregorian
    while current_date <= end_date_gregorian:
        # Convert current Gregorian date to Persian date
        persian_date = gregorian_to_persian(current_date.year, current_date.month, current_date.day)
        date_list.append(f"{persian_date[0]}/{persian_date[1]}/{persian_date[2]}")
        # Move to the next day
        current_date += timedelta(days=1)

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
    dropbox_download("https://www.dropbox.com/scl/fi/0l42qezrzs5iv3lubknuw/1403.xlsx?rlkey=ozjqny5i5o5gi98u5l073pimc&st=kuz4l70l&dl=0","farvardin")
    dropbox_download("https://www.dropbox.com/scl/fi/d1wux79gl92h9narou4xf/1403.xlsx?rlkey=sh5cljzhvpx2qcrhmln34vtwj&st=sk2kb5s2&dl=0", "ordibehesht")
    dropbox_download("https://www.dropbox.com/scl/fi/dlrfovoroyljqdketdcl9/1403.xlsx?rlkey=rk8p65pggu839rpupq39lz99z&st=kenx4ebp&dl=0", "khordad")
    dropbox_download("https://www.dropbox.com/scl/fi/yjnjon3k3r4fl1relw87j/1403.xlsx?rlkey=wrquyyhzs2i5hxp3q3zdyphmq&st=vqv9i4yv&dl=0", "tir")
    

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
        for i in df.index.to_list():
            try:
                df.loc[i,"تاریخ سفارش"] = convert_date(df.loc[i,"تاریخ سفارش"])
            except:
                continue

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


        ##  Creting Excel of cafes
        dict_1 = {}
        cafe_list = set(span_df["نام کافه"].to_list())
        for i in cafe_list:
            dict_1[i] = {}
            sf = span_df[span_df["نام کافه"] == i]
            for j in set(sf["نام محصول"].to_list()):
                gf = sum(sf[sf["نام محصول"]== j]["واحد فرعی"].to_list())/1000
                dict_1[i].update({j:gf})

        cafe_df = pd.DataFrame(dict_1).T
        cafe_df["Total"] = cafe_df.sum(axis=1)
        cafe_df = cafe_df.sort_values(by='Total', ascending=False)

        ##  Creting Excel of cities
        dict_2 = {}
        city_list = set(span_df["شهر"].to_list())
        for i in city_list:
            dict_2[i] = {}
            sf = span_df[span_df["شهر"] == i]
            for j in set(sf["نام محصول"].to_list()):
                gf = sum(sf[sf["نام محصول"]== j]["واحد فرعی"].to_list())/1000
                dict_2[i].update({j:gf})

        city_df = pd.DataFrame(dict_2).T
        city_df["Total"] = city_df.sum(axis=1)
        city_df = city_df.sort_values(by='Total', ascending=False)

        # Displaying plots
        st.markdown("<h5><div style='font-family: xav semibold; direction: ltr;'>  فروش به تفکیک سری</div>", unsafe_allow_html=True)
        plot_data(plot_dict, "")
        st.markdown("<h5><div style='font-family: xav semibold; direction: ltr;'>   V فروش سری</div>", unsafe_allow_html=True)
        plot_data(v_dict, "  ")
        st.markdown("<h5><div style='font-family: xav semibold; direction: ltr;'>   A فروش سری</div>", unsafe_allow_html=True)
        plot_data(a_dict, "        ")
        st.markdown("<h5><div style='font-family: xav semibold; direction: ltr;'>  X فروش سری</div>", unsafe_allow_html=True)
        plot_data(x_dict, "              ")
        st.markdown("<h5><div style='font-family: xav semibold; direction: ltr;'>فروش ۱۰ کافه اول</div>", unsafe_allow_html=True)
        plot_data(top_cafe_dict, "            ")
            # Button to download the Excel file
        excel_data = to_excel(cafe_df)
        st.download_button(label='Download Excel',
                        data=excel_data,
                        file_name=f'cafe_sell_{start_date}_{end_date}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        st.markdown("<h5><div style='font-family: xav semibold; direction: ltr;'>فروش ۱۰ شهر اول</div>", unsafe_allow_html=True)
        plot_data(top_city_dict, "           ")
        excel_data = to_excel(city_df)
        st.download_button(label='Download Excel',
                        data=excel_data,
                        file_name=f'city_sell_{start_date}_{end_date}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')





if __name__ == "__main__":
    main()
