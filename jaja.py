import streamlit as st
import pizza
import radar
import scatter
import rapport

# Set up the Streamlit app with a main header
st.markdown("<h1 style='font-size: 34px;'>Make Your Own Data Visualizations</h1>", unsafe_allow_html=True)

# Add a subtitle with adjusted margin for closer positioning
st.markdown("<h2 style='font-size: 16px; font-weight: normal; margin-top: -32px;'>Data Updated Weekly | By <a href='https://x.com/DanishScout_' target='_blank'>DanishScout</a> | <a href='https://buymeacoffee.com/danishscout' target='_blank'>Support My Work</a></h2>", unsafe_allow_html=True)

# Add a checkbox to show available leagues
if st.sidebar.checkbox("Show Available Leagues"):
    leagues = """
    - Superligaen
    - Allsvenskan
    - Eliteserien
    - Premier League
    - LaLiga
    - Bundesliga
    - Serie A
    - Ligue 1
    - Eredivisie
    - Liga Portugal
    - First Division A
    - Premiership
    - J. League
    - Liga Profesional
    - Brazilian Serie A
    - Austrian Bundesliga
    """
    st.sidebar.markdown(leagues)

# Add a horizontal line
st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# Use radio buttons for visualization selection
visualization_option = st.radio(
    "Choose which visualization to display:",
    ("Pizza Chart", "Radar Comparison", "Scatter Plot", "Match Report")
)

# Add a horizontal line
st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# Run the selected visualization
if visualization_option == "Pizza Chart":
    pizza.run()  # Assuming the pizza script has a run() function

elif visualization_option == "Radar Comparison":
    radar.run()

elif visualization_option == "Scatter Plot":
    scatter.run()

elif visualization_option == "Match Report":
    rapport.run()

