import streamlit as st

# Set the title of the dashboard

# Create a sidebar with a selectbox for sorting options
st.sidebar.title("Capacity Possibility")
sort_options = ["Max Happend", "Avg-Sorter", "Factory per day record", "highest record of factory in a day", "best sorter avg", "highest sort in a day"]
selected_option = st.sidebar.selectbox("Choose an option", sort_options)


import streamlit as st
def calculate_months_to_target_growth(starting_point, target_growth, monthly_growth_rate):
    months = 0
    current_value = starting_point
    while current_value < target_growth:
        current_value *= (1 + monthly_growth_rate)
        months += 1
    return months



# Sort section
st.header("Sort")
if selected_option == "Max Happend":
    st.metric("Capacity",value=4450)


elif selected_option == "Avg-Sorter":
    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
    input1 = st.slider("", 0, 30, 10, step=1)
    value = input1*362
    st.metric("Capacity",value=value)

elif selected_option == "Factory per day record":
    st.metric("Capacity",value=153*23)


elif selected_option == "highest record of factory in a day":
    st.metric("Capacity",value=360*23)

elif selected_option == "best sorter avg":
    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
    input1 = st.slider("", 0, 30, 10, step=1)
    value = input1*23*23.71
    st.metric("Capacity",value=value)

elif selected_option == "highest sort in a day":
    st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
    input1 = st.slider("", 0, 30, 10, step=1)
    value = input1*41.4*23
    st.metric("Capacity",value=value)


import streamlit as st

def calculate_months_to_target_growth(starting_point, target_growth, monthly_growth_rate):
    months = 0
    current_value = starting_point
    while current_value < target_growth:
        current_value *= (1 + monthly_growth_rate)
        months += 1
    return months

import streamlit as st


starting_point = st.number_input('Enter the starting point (current sales):', min_value=3000, max_value=5000, step=1, value=3000)
target_growth = st.number_input('Enter the target sales growth:', min_value=starting_point+1, max_value=10000, step=1, value=4000)
monthly_growth_rate = st.slider('Select the monthly growth rate:', min_value=0.01, max_value=0.20, step=0.01, value=0.05)

if st.button('Calculate'):
    months_needed = calculate_months_to_target_growth(starting_point, target_growth, monthly_growth_rate)
    st.write(f'{months_needed} Months')