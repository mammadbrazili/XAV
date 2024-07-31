import streamlit as st
import streamlit as st
import pandas as pd
import streamlit as st
import random
import os 
import requests
import openpyxl
import altair as alt
import base64
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

load_black()
load_bold()

st.markdown("<h1 style='text-align: center; font-family: xav black;'>فرم نظرسنجی کافه</h3>", unsafe_allow_html=True)
# Section 1
st.markdown("<h2><div style='font-family: xav semibold; direction: ltr;'>سرو قهوه</div>", unsafe_allow_html=True)
q1_1 = st.checkbox("تفاوت رسپی با پتانسیل", key="q1_1")
q1_2 = st.checkbox("شناخت و پرزنت قهوه", key="q1_2")
q1_3 = st.checkbox("استفاده از ظروف مناسب", key="q1_3")
st.write("------------------------------------------------------------------------------------------------------")

# Section 2
st.markdown("<h2><div style='font-family: xav semibold; direction: ltr;'>باریستا</div>", unsafe_allow_html=True)
q2_1 = st.checkbox("تئوری", key="q2_1")
q2_2 = st.checkbox("عملی", key="q2_2")
q2_3 = st.checkbox("پیگیری باریستا", key="q2_3")
st.write("------------------------------------------------------------------------------------------------------")


# Section 3
st.markdown("<h2><div style='font-family: xav semibold; direction: ltr;'>نگهداری و نظافت</div>", unsafe_allow_html=True)
q3_1 = st.checkbox("شرایط و نگهداری و قهوه", key="q3_1")
q3_2 = st.checkbox("سلامت تجهیزات", key="q3_2")
q3_3 = st.checkbox("سلامت محیط کار", key="q3_3")
st.write("------------------------------------------------------------------------------------------------------")

# Section 4
st.markdown("<h2><div style='font-family: xav semibold; direction: ltr;'>نحوه ارائه قهوه تخصصی</div>", unsafe_allow_html=True)
q4_1 = st.checkbox("ارزش گذاری", key="q4_1")
q4_2 = st.checkbox("نحوه پرزنت", key="q4_2")

# Define the scores for each question
scores = {
    "q1_1": 20, "q1_2": 20, "q1_3": 5,
    "q2_1": 15, "q2_2": 15, "q2_3": 5,
    "q3_1": 8, "q3_2": 7, "q3_3": 5,
    "q4_1": 6, "q4_2": 4
}

# Calculate the total score based on selected checkboxes
total_score = 0
if q1_1:
    total_score += scores["q1_1"]
if q1_2:
    total_score += scores["q1_2"]
if q1_3:
    total_score += scores["q1_3"]
if q2_1:
    total_score += scores["q2_1"]
if q2_2:
    total_score += scores["q2_2"]
if q2_3:
    total_score += scores["q2_3"]
if q3_1:
    total_score += scores["q3_1"]
if q3_2:
    total_score += scores["q3_2"]
if q3_3:
    total_score += scores["q3_3"]
if q4_1:
    total_score += scores["q4_1"]
if q4_2:
    total_score += scores["q4_2"]

total_score = int(total_score/11*10)

# Display the total score when the submit button is clicked
if st.button("ارسال"):
    st.subheader("نتیجه")
    if total_score <50 :
        st.write(f"امتیاز کل: {total_score} ")
        st.write("V Series Cafe")
        
    elif total_score > 50 and total_score<80  :
        st.write(f"امتیاز کل: {total_score} ")
        st.write("A Series Cafe")
        
    else:
        st.write(f"امتیاز کل: {total_score} ")
        st.write("X Series Cafe")

