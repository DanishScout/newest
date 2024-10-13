import streamlit as st
import pizza
import radar
import scatter
import rapport

# Set up the Streamlit app with a main header
st.markdown("<h1 style='font-size: 34px;'>Make Your Own Data Visualizations</h1>", unsafe_allow_html=True)

# Add a subtitle with adjusted margin for closer positioning
st.markdown("<h2 style='font-size: 16px; font-weight: normal; margin-top: -32px;'>Data Updated Weekly | By <a href='https://x.com/DanishScout_' target='_blank'>DanishScout</a> | <a href='https://buymeacoffee.com/danishscout' target='_blank'>Support My Work</a></h2>", unsafe_allow_html=True)

# Add a horizontal line
st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# Add a title for the app in the main area
st.sidebar.title("Select Visualization")

# Add a dropdown for user selection of visualization in the main area
visualization_option = st.sidebar.selectbox(
    "Choose which visualization to display:",
    ("pizza", "radar", "scatter", "rapport")
)

# Run the selected visualization
if visualization_option == "pizza":
    pizza.run()  # Assuming the pizza script has a run() function

elif visualization_option == "radar":
    radar.run()

elif visualization_option == "scatter":
    scatter.run()

elif visualization_option == "rapport":
    rapport.run()
