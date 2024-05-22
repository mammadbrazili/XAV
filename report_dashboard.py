import streamlit as st
import pandas as pd
import streamlit as st
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, Label
import random
import os 

relative_path = '~/Dropbox/XAV coffee works/XAV Revenue/Excels/1403/بهار 1403/01 - فروردین/سفارشات کالا فروردین 1403.xlsx'
full_path_1 = os.path.expanduser(relative_path)
full_path_2 = os.path.expanduser("~/Dropbox/XAV coffee works/XAV Revenue/Excels/1403/بهار 1403/02 - اردیبهشت/سفارشات کالا اردیبهشت 1403.xlsx")


# Function to read and concatenate excel files
def read_excel_files():
    df1 = pd.concat(pd.read_excel(full_path_1, sheet_name=None), ignore_index=True)
    df2 = pd.concat(pd.read_excel(full_path_2,sheet_name=None),ignore_index=True)
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

# Function to plot data
def plot_data(dict1, string):
    x = list(dict1.keys())
    y = list(dict1.values())
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(len(x))]
    source = ColumnDataSource(data=dict(x=x, y=y, color=colors))
    p = figure(x_range=x, height=600, width=1000, title=f"Each {string} Sale This Week", toolbar_location=None, tools="")
    p.vbar(x='x', top='y', width=0.5, source=source, color="color")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 45
    x_offset = 40 if len(x) > 9 else [350, 220, 70, 110, 85, 70, 40, 55, 40][len(x) - 1]
    for i, value in enumerate(y):
        label = Label(x=i, y=value, text=str(round(value, 2)), text_baseline='middle', text_align='center', text_font_size="8pt", x_offset=x_offset, y_offset=10)
        p.add_layout(label)
    return p

# Streamlit app
def main():
    st.title("XAV Coffee Works Report Generator")

    # User inputs for start and end date
    start_date = st.text_input("Start date of report (YYYY/MM/DD):")
    end_date = st.text_input("End date of report (YYYY/MM/DD):")

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
        st.bokeh_chart(plot_data(plot_dict, "Series"))
        st.bokeh_chart(plot_data(v_dict, "V Series"))
        st.bokeh_chart(plot_data(a_dict, "A Series"))
        st.bokeh_chart(plot_data(x_dict, "X Series"))
        st.bokeh_chart(plot_data(top_cafe_dict, "Cafe"))
        st.bokeh_chart(plot_data(top_city_dict, "City"))

if __name__ == "__main__":
    main()
