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
import numpy as np
import streamlit.components.v1 as components

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

load_bold()
load_black()

df = pd.read_excel("/Users/mohammad/XAV/Departemant Media/Recap/Coffee Data.xlsx")

# creating a function to create a map for countries


def download_geojson(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")
        return False

def get_country_center(country_geojson):
    """
    Calculate the center coordinates of a country polygon.
    """
    country_coordinates = country_geojson['geometry']['coordinates']
    if country_geojson['geometry']['type'] == 'Polygon':
        country_coordinates = [country_coordinates]
    lats = [coord[1] for poly_coords in country_coordinates for coord in poly_coords[0]]
    lons = [coord[0] for poly_coords in country_coordinates for coord in poly_coords[0]]
    lat = sum(lats) / len(lats)
    lon = sum(lons) / len(lons)
    return [lat, lon]

def color_country_map(country_names):
    # Create a map centered around the world
    world_map = folium.Map(location=[0, 0], zoom_start=2)
    
    # Download the GeoJSON file containing country boundaries
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    geo_json_data = 'world-countries.json'
    if not download_geojson(url, geo_json_data):
        return None
    
    # Generate a random color for each country
    country_colors = {}
    for country_name in country_names:
        country_colors[country_name] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
    # Color all specified countries with random colors and add flag icons
    for country_name in country_names:
        flag_icon = f"/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/{country_name}.png"  # Assuming the flags are named after the country
        country_geojson = next((country for country in folium.features.GeoJson(geo_json_data).data['features'] if country['properties']['name'] == country_name), None)
        if country_geojson:
            center = get_country_center(country_geojson)
            folium.Marker(
                location=center,
                icon=folium.CustomIcon(flag_icon, icon_size=(20, 20)),
                popup=country_name
            ).add_to(world_map)
        
    # Color the countries
    folium.GeoJson(
        geo_json_data,
        name='geojson',
        style_function=lambda feature: {
            'fillColor': country_colors[feature['properties']['name']] if feature['properties']['name'] in country_names else 'None',
            'color': 'black',
            'weight': 1.5,
            'fillOpacity': 0.7
        }
    ).add_to(world_map)

    return world_map



#-------------------------------------------------------------- MAIN PAGE -------------------------------------------------------------------

def page_home():
    load_black()
    load_bold()
    st.markdown("<h1><div style='font-family: xav black; direction: rtl;'>X                   A                   V</div>", unsafe_allow_html=True)
    st.write("---------------------------------------------------------")
    st.markdown("<h1><div style='font-family: xav black; direction: rtl;'>گزارش اسفند و فروردین دپارتمان مالی</div>", unsafe_allow_html=True)
    st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'> مباحث این گزارش;  </div>", unsafe_allow_html=True)
    

    load_black()

    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 28px; margin-right: 40px;'>بررسی اطلاعات قهوه‌ها در سالی که گذشت</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)


    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 22px; margin-right:76px;'>خاستگاه‌ها</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)

    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 22px; margin-right:76px;'>فرآوری‌ها</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)

    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 22px; margin-right:76px;'>پرفروش‌ترین‌ها</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)



    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 28px; margin-right: 40px;'>بررسی ظرفیت‌ و ماکسیمم تولید</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)

    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 22px; margin-right:76px;'>ظرفیت تولید تحت شرایط مختلف</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)

    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 22px; margin-right:76px;'>چگونه به ظرفیت تولید برسیم؟</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)


    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 28px; margin-right: 40px;'> تاثیر هر بخش تولید بر بهای تمام شده</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)

    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 22px; margin-right:76px;'>به تفکیک سری</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)

    bullet_pointed_heading = """
    <ul style='list-style-type: disc; direction: rtl;'>
        <li style='font-family: xav semibold; font-size: 22px; margin-right:76px;'>به تفکیک خاستگاه</li>
    </ul>
    """
    st.markdown(bullet_pointed_heading, unsafe_allow_html=True)

#-------------------------------------------------------------- COFFEE DATA Page -------------------------------------------------------------------

def page_about():
    load_bold()
    load_black()
    st.markdown("<h1><div style='font-family: xav semibold; direction: rtl;'>  اطلاعات قهوه   </div>", unsafe_allow_html=True)
    # st.write("Financial Departemant Report \n \n ")
    st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'> نقشه خاستگاه‌ها  </div>", unsafe_allow_html=True)


    # defining algorithm for  option "Total"
    def algorithm_option1():
        countries = list(set(df["Country"].to_list()))
        countries.remove("Vortex")
        map = color_country_map(countries)
        map.save("map.html")
        with open("map.html", "r") as f:
            folium_map = f.read()
        components.html(folium_map, height=500)

     
    # Function to execute algorithm for Option "X Series"
    def algorithm_option2():
        gf = df[df["Serie"]=="X Series"]
        countries = list(set(gf["Country"].to_list()))
        map = color_country_map(countries)
        map.save("map.html")
        with open("map.html", "r") as f:
            folium_map = f.read()
        components.html(folium_map, height=500)

    # Function to execute algorithm for Option "A Series"
    def algorithm_option3():
        gf = df[df["Serie"] == "A Series"]
        countries = list(set(gf["Country"].to_list()))
        map = color_country_map(countries)
        map.save("map.html")
        with open("map.html", "r") as f:
            folium_map = f.read()
        components.html(folium_map, height=500)

    # Function to execute algorithm for Option "V Series"
    def algorithm_option4():
        load_black()
        load_bold()
        gf = df[df["Serie"] == "V Series"]
        countries = list(set(gf["Country"].to_list()))
        countries.remove("Vortex")
        map = color_country_map(countries)
        map.save("map.html")
        with open("map.html", "r") as f:
            folium_map = f.read()
        components.html(folium_map, height=500)

        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'></div>", unsafe_allow_html=True)

        st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'> ۱۰ لاین  </div>", unsafe_allow_html=True)
        st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'> ۷ کشور  </div>", unsafe_allow_html=True)
        st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'> ۴ قهوه با فرآوری شسته و ۶ قهوه با فرآوری طبیعی  </div>", unsafe_allow_html=True)
        st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'>طعم‌یادهای پرفروش به ترتیب میوه‌ای شیرین و آجیلی بودند </div>", unsafe_allow_html=True)
        st.markdown("<h3><div style='font-family: xav semibold; direction: rtl;'></div>", unsafe_allow_html=True)



    # Add an expander
    with st.expander(""):
        
        # Add selectbox to choose between options
        option = st.selectbox("Choose a Serie", ["Total", "X", "A", "V"])

                # Execute algorithm based on selected option
        if option == "Total":
            algorithm_option1()
        elif option == "X":
            algorithm_option2()
        elif option == "A":
            algorithm_option3()
        elif option == "V":
            algorithm_option4()



#-------------------------------------------------------------- CAPACITY PAGE -------------------------------------------------------------------

def page_contact():
    st.markdown("<h1><div style='font-family: xav semibold; direction: rtl;'>  ظرفیت تولید  </div>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; font-family: xav semibold;'>فقط سورت دستی</h3>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
    input1 = st.slider("", 0, 30, 10, step=1)
    st.markdown("<h1 style='text-align: center; font-family: xav semibold;'> وضعیت فعلی</h3>", unsafe_allow_html=True)


#-------------------------------------------------------------- COST PAGE -------------------------------------------------------------------
def cost_page():

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
            textinfo="value",
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



#-------------------------------------------------------------- Setting of PAGE -------------------------------------------------------------------
   


def main():
    st.sidebar.title("مسیر")
    page = st.sidebar.radio("انتخاب صفحه", ["صفحه‌اصلی", "اطلاعات قهوه" ,"ظرفیت تولید", "هزینه تولید"])

    if page == "صفحه‌اصلی":
        page_home()
    elif page == "اطلاعات قهوه":
        page_about()
    elif page == "ظرفیت تولید":
        page_contact()

    else:
        cost_page()


if __name__ == "__main__":
    main()






