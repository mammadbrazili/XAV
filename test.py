import streamlit as st
import matplotlib.pyplot as plt

def plot(df,metric):
    # Sample data
    categories = df.index
    values = df[metric].to_list()

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Create a bar chart
    bars = ax.bar(categories, values)

    # Set the colors of the bars
    for bar in bars:
        bar.set_color('#3498db')  # Sharp blue color

    # Set the title and labels
    ax.set_title('Bar Chart Example')
    ax.set_xlabel('Categories') 
    ax.set_ylabel('Values')

    # Show the exact values on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{height}', ha='center', va='bottom')

    # Show the plot in Streamlit
    st.pyplot(fig)
