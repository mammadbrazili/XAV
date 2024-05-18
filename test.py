import streamlit as st
import folium
import streamlit.components.v1 as components

def main():
    # Set up your Streamlit app title
    st.title("Folium Map in Streamlit")

    # Create a Folium map
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

    # Add markers, polygons, or other layers to your Folium map if needed
    folium.Marker([40.7128, -74.0060], popup="New York City").add_to(m)

    # Save the Folium map to an HTML file
    m.save("map.html")

    # Read the HTML file and display it in the Streamlit app
    with open("map.html", "r") as f:
        folium_map = f.read()

    # Display the Folium map in Streamlit using components.html
    components.html(folium_map, height=500)

if __name__ == "__main__":
    main()
