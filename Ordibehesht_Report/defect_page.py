import streamlit as st

# Set the title of the dashboard

# Create a sidebar with a selectbox for sorting options
st.sidebar.title("Capacity Possibility")
sort_options = ["Max Happend", "Avg-Sorter", "Factory per day record", "highest record of factory in a day", "best sorter avg", "highest sort in a day"]
selected_option = st.sidebar.selectbox("Choose an option", sort_options)

# Create the main content area

# Roast section
st.header("Roast")

st.write("20-25 Batch Daily Besca 5Kg:")
st.write("25-30 Batch Daily Gizen 12kg")

option = st.selectbox(
    "Select Roast Level:",
    ("Low", "Moderate", "High")
)

if option == "Low":
    st.metric("Capacity", value=9200)
elif option == "High":
    st.metric("Capacity", value=111555)
else:
    st.write("Moderate:")
    st.metric("Capacity", value=9982)


# # Sort section
# st.header("Sort")
# if selected_option == "Max Happend":
#     st.metric("Capacity",value=4450)


# elif selected_option == "Avg-Sorter":
#     st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
#     input1 = st.slider("", 0, 30, 10, step=1)
#     value = input1*362
#     st.metric("Capacity",value=value)

# elif selected_option == "Factory per day record":
#     st.metric("Capacity",value=153*23)


# elif selected_option == "highest record of factory in a day":
#     st.metric("Capacity",value=360*23)

# elif selected_option == "best sorter avg":
#     st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
#     input1 = st.slider("", 0, 30, 10, step=1)
#     value = input1*23*23.71
#     st.metric("Capacity",value=value)

# elif selected_option == "highest sort in a day":
#     st.markdown("<h4 style='text-align: right; font-family: xav semibold; direction: rtl;'>تعداد سورتر</h4>", unsafe_allow_html=True)
#     input1 = st.slider("", 0, 30, 10, step=1)
#     value = input1*41.4*23
#     st.metric("Capacity",value=value)
