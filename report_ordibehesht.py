import streamlit as st
import pandas as pd
import folium
import requests
import random
import webbrowser
from streamlit_folium import folium_static
import base64
from PIL import Image
import os

# Using XAV Type Face

def load_black():
    font_file_path = "/Users/mohammad/Library/Fonts/xav black.ttf"
    with open(font_file_path, "rb") as font_file:
        font_data = font_file.read()
    encoded_font = base64.b64encode(font_data).decode("utf-8")
    css = f"@font-face {{ font-family: 'xav black'; src: url('data:application/octet-stream;base64,{encoded_font}'); }}"
    st.write('<style>{}</style>'.format(css), unsafe_allow_html=True)

def load_bold():
    font_file_path = "/Users/mohammad/Library/Fonts.ttf"
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
        folium_static(map)

     
    # Function to execute algorithm for Option "X Series"
    def algorithm_option2():
        gf = df[df["Serie"]=="X Series"]
        countries = list(set(gf["Country"].to_list()))
        map = color_country_map(countries)
        folium_static(map)

    # Function to execute algorithm for Option "A Series"
    def algorithm_option3():
        gf = df[df["Serie"] == "A Series"]
        countries = list(set(gf["Country"].to_list()))
        map = color_country_map(countries)
        folium_static(map)

    # Function to execute algorithm for Option "V Series"
    def algorithm_option4():
        load_black()
        load_bold()
        gf = df[df["Serie"] == "V Series"]
        countries = list(set(gf["Country"].to_list()))
        countries.remove("Vortex")
        map = color_country_map(countries)
        folium_static(map)
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
    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>میانگین سورت در هر روز </h4>", unsafe_allow_html=True)
    input2 = st.slider(" ", 10, 100, 40)
    capacity_1 = input1*input2* 25
    st.metric(label="", value=capacity_1)


    # Possibility 2: 2 float inputs
    st.markdown("<h3 style='text-align: center; font-family: xav semibold;'>فقط سورت ماشینی</h3>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'> ظرفیت دسگاه سورت جدید در روز</h4>", unsafe_allow_html=True)
    input3 = st.slider("", 100, 1100, 150)
    capacity_1 = input3* 25
    st.metric(label="", value=capacity_1)

    # Possibility 3: 4 float inputs
    st.markdown("<h3 style='text-align: center; font-family: xav semibold;'> دستگاه سورت  +  سورت دستی</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
    input1 = st.slider("         ", 0, 30, 10, step=1)
    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>میانگین سورت در هر روز </h4>", unsafe_allow_html=True)
    input2 = st.slider("    ", 10, 100, 40)
    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'> ظرفیت دسگاه سورت جدید در روز</h4>", unsafe_allow_html=True)
    input3 = st.slider("                     ", 100, 1100, 150)
    capacity_1 = input3* 25 + (input1*input2* 25)
    st.metric(label="", value=capacity_1)


    st.markdown("<h1 style='text-align: center; font-family: xav semibold;'> وضعیت فعلی</h3>", unsafe_allow_html=True)


#-------------------------------------------------------------- COST PAGE -------------------------------------------------------------------
def cost_page():

        # check
        # Add options in the sidebar
    option = st.sidebar.selectbox(
        '',
        ('برحسب سری', 'برحسب خاسنگاه')
)
    if option == 'برحسب سری':
        st.markdown('<h1 style="text-align: center;">Flags</h1>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)

    else:
        st.markdown("<h1 style='text-align: center; font-family: xav semibold;'> میزان بهای از دست رفته </h3>", unsafe_allow_html=True)
        st.write("----------------------------------------------------------------------------------------")
        # Your DataFrame
        data = {
            0: ['Peru', 'El Salvador', 'Ethiopia', 'Brazil', 'Costa Rica', 'Honduras', 'Colombia', 'Kenya', 'Rwanda', 'Panama', 'Guatemala'],
            1: [0.8562, 0.8488, 0.8669, 0.8624, 0.8603, 0.8596, 0.8463, 0.8555, 0.8549, 0.8628, 0.8575]
        }

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(data).rename(columns={0: 'Country', 1: 'Value'})

        # Sort the DataFrame by the 'Value' column in descending order
        sorted_df = df.sort_values(by='Value', ascending=False)


        # Create a dictionary mapping country names to their flag filenames
        flag_mapping = {
            'Peru': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Peru.png',
            'El Salvador': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/El Salvador.png',
            'Ethiopia': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Ethiopia.png',
            'Brazil': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Brazil.png',
            'Costa Rica': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Costa Rica.png',
            'Honduras': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Honduras.png',
            'Colombia': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Colombia.png',
            'Kenya': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Kenya.png',
            'Rwanda': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Rwanda.png',
            'Panama': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Panama.png',
            'Guatemala': '/Users/mohammad/XAV/Departemant Financial/Report Esfand Farvardin/flags/Guatemala.png'
        }

        # Replace country names with flag filenames
        sorted_df['Country'] = sorted_df['Country'].map(flag_mapping)

        # Display the DataFrame with flag images in your Streamlit app
        for index, row in sorted_df.iterrows():
            st.image(row['Country'], width=100)
            st.markdown('<h2 class="right">{}</h2>'.format(round(1 - (row['Value']*0.92*0.97),3)), unsafe_allow_html=True)
            st.write("----------------------------------------------------------------------------------------")


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






