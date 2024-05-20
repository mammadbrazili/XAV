import streamlit as st
import pandas as pd
import folium
import requests
import random
import webbrowser
import base64
from PIL import Image
import os
import folium
import streamlit.components.v1 as components
import numpy as np

dataset = pd.read_excel("/Users/mohammad/Dropbox/XAV Finance (1)/گزارشات/1403/اردیبهشت/اطلاعات قهوه.xlsx").iloc[:26]
#--------------------------------------------------------- Functions Defining ---------------------------------------------------------------
total_roast = sum(dataset["each_line_sum"].to_list())

def filter(Metric):

    series_dict = {}
    for i in set(dataset[Metric].to_list()):
        gf = dataset[dataset[Metric] == i]
        total_kg = sum(gf["each_line_sum"] .to_list())
        total_share = total_kg / total_roast
        gb_roast_defect_rate = np.mean(gf["gb_roast_defect_rate"].to_list())
        gb_roast_baha = np.mean(gf["gb_roast_baha"].to_list())
        roast_sort1_defect_rate = np.mean(gf["roast_sort1_defect_rate"].to_list())
        roast_sort1_baha = np.mean(gf["roast_sort1_baha"].to_list())
        sort1_sort2_defect_rate = np.mean(gf["sort1_sort2_defect_rate"].to_list())
        sort1_sort2_baha = np.mean(gf["sort1_sort2_baha"].to_list())
        gb_pack_defect_rate = np.mean(gf["gb_pack_defect_rate"].to_list())
        gb_pack_baha = np.mean(gf["gb_pack_baha"].to_list())
        roasted =  np.mean(gf["Roasted"].to_list())
        sorted =  np.mean(gf["Sorted"].to_list())
        sorted_2 =  np.mean(gf["Sorted2"].to_list())

        line = len(gf)

        series_dict[i] = [line,total_kg,total_share,gb_roast_defect_rate,gb_roast_baha,roast_sort1_defect_rate,roast_sort1_baha,
                        sort1_sort2_defect_rate,sort1_sort2_baha,gb_pack_defect_rate,gb_pack_baha,roasted,sorted,sorted_2]

        final = pd.DataFrame(series_dict).T
        final.columns = ['lines', 'Total_GB', 'Share_of_Total', '‌GB_to_Roast', 'GB_Roast_Baha', 'Roast_Sort1',
            'Roast_Sort1_Baha', 'Sort1_Sort2', 'Sort1_Sort2_baha', 'GB_Final', 'GB_Final_Baha',"roasted","sorted","sorted_2"]

    return final



import streamlit as st
import matplotlib.pyplot as plt
import random

import streamlit as st
import matplotlib.pyplot as plt
import random

def plot(df, metric):
    # Sample data
    categories = df.index
    values = df[metric].to_list()

    # Create a figure and axis with a bigger size
    fig, ax = plt.subplots(figsize=(60, 48))

    # Create a bar chart
    bars = ax.bar(categories, values)

    # Set the colors of the bars randomly from a larger palette
    colors = ['#ADD8E6', '#CCCCFF', '#D8BFD8', '#E6E6FA', '#87CEEB', '#B0C4DE', '#9370DB', '#8470FF', '#BA55D3', '#DA70D6',
            '#00BFFF', '#1E90FF', '#6495ED', '#7B68EE', '#4169E1', '#0000FF', '#4682B4', '#00CED1', '#00FFFF', '#00FA9A']
    for bar, color in zip(bars, random.choices(colors, k=len(bars))):
        bar.set_color(color)


    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=50)
    ax.tick_params(axis='y', labelsize=50)

    # Show the exact values on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{round(height,3)} ', ha='center', va='bottom', fontsize=45)

    # Show the plot in Streamlit
    st.pyplot(fig)



import plotly.graph_objects as go

def funnel(level_data,string):

    # Define colors for each level
    level_colors = ['#FF5733', '#33FF57', '#5733FF', '#33FFC0', '#FF33C0']


    # Create the funnel chart using go.Funnel
    fig = go.Figure(go.Funnel(
        y=list(level_data.keys()),
        x=list(level_data.values()),
        textinfo="value"[:5],
        marker={"color": level_colors}
    ))

    # Update layout to make the plot bigger and display values
    fig.update_layout(width=600, height=600, bargap=0.1)
    fig.update_traces(textposition="inside")
    fig.update_layout(
    title={
        'text': f"{string}",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    title_font=dict(
        size=14,
        color='blue',
        family='Arial'
    )
)


    # Show the plot
    st.plotly_chart(fig)








def main():
    st.title(" ")

    # Main options
    main_options = ["لاین", "سری", "خاستگاه", "رقم", "فرآوری"]
    selected_main_option = st.selectbox(" ", main_options)
    sub_options = ["line",'Total_GB', 'Share_of_Total', 'Defect Rates', "Cost"]
    selected_sub_option = st.selectbox("", sub_options)


    # Sub-options based on the selected main option
    #---------------------------------------
    if selected_main_option == "لاین":
        df = filter("Name")

        if selected_sub_option == "Total_GB":
            plot(df,"Total_GB")


        elif selected_sub_option == "Share_of_Total":
            plot(df,"Share_of_Total")

        elif selected_sub_option ==  "Defect Rates":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : df.loc[i,"‌GB_to_Roast"] ,  "Roast_Sort1" : df.loc[i,"Roast_Sort1"] , "Sort1_Sort2" : df.loc[i,"Sort1_Sort2"] ,
                            "GB_Final" : df.loc[i,"GB_Final"] }
                funnel(data_dict,i)

        elif selected_sub_option ==  "Cost":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : (100/(df.loc[i,"‌GB_to_Roast"]))-100 ,  "Roast_Sort1" : (100/(df.loc[i,"Roast_Sort1"]))-100 ,
                            "Sort1_Sort2" : (100/(df.loc[i,"Sort1_Sort2"]))-100 ,
                            "GB_Final" : (100/ (df.loc[i,"GB_Final"]))-100 }
                funnel(data_dict,i)



#---------------------------------------
    elif selected_main_option == "سری":
        sub_options = ["line",'Total_GB', 'Share_of_Total', 'Defect Rates', "Cost"]

        df = filter("Series")

        if selected_sub_option == "line":
            plot(df,"lines")

        elif selected_sub_option == "Total_GB":
            plot(df,"Total_GB")

        elif selected_sub_option == "Share_of_Total":
            plot(df,"Share_of_Total")


        elif selected_sub_option ==  "Defect Rates":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : df.loc[i,"‌GB_to_Roast"] ,  "Roast_Sort1" : df.loc[i,"Roast_Sort1"] , "Sort1_Sort2" : df.loc[i,"Sort1_Sort2"] ,
                            "GB_Final" : df.loc[i,"GB_Final"] }
                funnel(data_dict,i)

        elif selected_sub_option ==  "Cost":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : (100/(df.loc[i,"‌GB_to_Roast"]))-100 ,  "Roast_Sort1" : (100/(df.loc[i,"Roast_Sort1"]))-100 ,
                            "Sort1_Sort2" : (100/(df.loc[i,"Sort1_Sort2"]))-100 ,
                            "GB_Final" : (100/ (df.loc[i,"GB_Final"]))-100 }
                funnel(data_dict,i)

#---------------------------------------

    elif selected_main_option == "خاستگاه":
        sub_options = ["line",'Total_GB', 'Share_of_Total', 'Defect Rates', "Cost"]
        df = filter("Country")
        
        if selected_sub_option == "line":
            plot(df,"lines")

        elif selected_sub_option == "Total_GB":
            plot(df,"Total_GB")

        elif selected_sub_option == "Share_of_Total":
            plot(df,"Share_of_Total")


        elif selected_sub_option ==  "Defect Rates":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : df.loc[i,"‌GB_to_Roast"] ,  "Roast_Sort1" : df.loc[i,"Roast_Sort1"] , "Sort1_Sort2" : df.loc[i,"Sort1_Sort2"] ,
                            "GB_Final" : df.loc[i,"GB_Final"] }
                funnel(data_dict,i)

        elif selected_sub_option ==  "Cost":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : (100/(df.loc[i,"‌GB_to_Roast"]))-100 ,  "Roast_Sort1" : (100/(df.loc[i,"Roast_Sort1"]))-100 ,
                            "Sort1_Sort2" : (100/(df.loc[i,"Sort1_Sort2"]))-100 ,
                            "GB_Final" : (100/ (df.loc[i,"GB_Final"]))-100 }
                funnel(data_dict,i)


#---------------------------------------

    elif selected_main_option == "رقم":
        df = filter("Variety")
        sub_options = ["line",'Total_GB', 'Share_of_Total', 'Defect Rates', "Cost"]

        if selected_sub_option == "line":
            plot(df,"lines")

        elif selected_sub_option == "Total_GB":
            plot(df,"Total_GB")

        elif selected_sub_option == "Share_of_Total":
            plot(df,"Share_of_Total")

        elif selected_sub_option ==  "Defect Rates":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : df.loc[i,"‌GB_to_Roast"] ,  "Roast_Sort1" : df.loc[i,"Roast_Sort1"] , "Sort1_Sort2" : df.loc[i,"Sort1_Sort2"] ,
                            "GB_Final" : df.loc[i,"GB_Final"] }
                funnel(data_dict,i)

        elif selected_sub_option ==  "Cost":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : (100/(df.loc[i,"‌GB_to_Roast"]))-100 ,  "Roast_Sort1" : (100/(df.loc[i,"Roast_Sort1"]))-100 ,
                            "Sort1_Sort2" : (100/(df.loc[i,"Sort1_Sort2"]))-100 ,
                            "GB_Final" : (100/ (df.loc[i,"GB_Final"]))-100 }
                funnel(data_dict,i)




#---------------------------------------

    elif selected_main_option == "فرآوری":
        df = filter("Proccess")

        sub_options = ["line",'Total_GB', 'Share_of_Total', 'Defect Rates', "Cost"]

        if selected_sub_option == "line":
            plot(df,"lines")

        elif selected_sub_option == "Total_GB":
            plot(df,"Total_GB")

        elif selected_sub_option == "Share_of_Total":
            plot(df,"Share_of_Total")


        elif selected_sub_option ==  "Defect Rates":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : df.loc[i,"‌GB_to_Roast"] ,  "Roast_Sort1" : df.loc[i,"Roast_Sort1"] , "Sort1_Sort2" : df.loc[i,"Sort1_Sort2"] ,
                            "GB_Final" : df.loc[i,"GB_Final"] }
                funnel(data_dict,i)

        elif selected_sub_option ==  "Cost":
            for i in df.index.to_list():
                data_dict = {"GB_Roast" : (100/(df.loc[i,"‌GB_to_Roast"]))-100 ,  "Roast_Sort1" : (100/(df.loc[i,"Roast_Sort1"]))-100 ,
                            "Sort1_Sort2" : (100/(df.loc[i,"Sort1_Sort2"]))-100 ,
                            "GB_Final" : (100/ (df.loc[i,"GB_Final"]))-100 }
                funnel(data_dict,i)


# -------------------------------------------------------

if __name__ == "__main__":
    main()
