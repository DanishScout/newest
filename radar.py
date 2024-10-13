import requests
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import numpy as np
import streamlit as st
import matplotlib.font_manager as fm
import os
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Font paths
font_path = "Alexandria-Regular.ttf"
font_pathh = "Alexandria-SemiBold.ttf"


# Load the font using FontProperties
custom_font = fm.FontProperties(fname=font_path)
custom_fontt = fm.FontProperties(fname=font_pathh)

# Load the new CSV files
df1 = pd.read_csv('den1.csv')
df2 = pd.read_csv('swe1.csv')
df3 = pd.read_csv('nor1.csv')
df4 = pd.read_csv('eng1.csv')
df5 = pd.read_csv('ger1.csv')
df6 = pd.read_csv('fra1.csv')
df7 = pd.read_csv('ita1.csv')
df8 = pd.read_csv('spa1.csv')
df9 = pd.read_csv('por1.csv')
df10 = pd.read_csv('ned1.csv')
df11 = pd.read_csv('bel1.csv')
df12 = pd.read_csv('sco1.csv')
df13 = pd.read_csv('jap1.csv')
df14 = pd.read_csv('arg1.csv')
df15 = pd.read_csv('bra1.csv')
df16 = pd.read_csv('aut1.csv')

# Combine the dataframes
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16], ignore_index=True)

# Filter players with at least 150 minutes played
df = df[df['Minutes Played'] >= 150]

# Filter players based on the specified leagues
valid_leagues = ['Superligaen', 'Allsvenskan', 'Eliteserien', 'Premier League', 'LaLiga',
                 'Bundesliga', 'Serie A', 'Ligue 1', 'Eredivisie', 'Liga Portugal', 'First Division A',
                 'Premiership', 'J. League', 'Liga Profesional', 'Brazilian Serie A', 'Austrian Bundesliga']
df = df[df['League'].isin(valid_leagues)]

# Available metrics categorized with display names only
available_metrics = {
    "Shooting": {
        "Goals": "Goals",
        "xG": "xG",
        "xG excl. penalty": "npxG",
        "xGOT": "xGOT",
        "Shots": "Shots",
        "Shots on target": "Shots\nOn Target"
    },
    "Passing": {
        "Assists": "Assists",
        "xA": "xA",
        "Chances created": "Chances\nCreated",
        "Accurate passes": "Accurate\nPasses",
        "Pass accuracy": "Pass\nAccuracy %",
        "Accurate long balls": "Accurate\nLong Balls",
        "Long ball accuracy": "Long Ball\nAccuracy %",
        "Successful crosses": "Successful\nCrosses",
        "Cross accuracy": "Cross\nAccuracy %"
    },
    "Possession": {
        "Dribbles": "Successful\nDribbles",
        "Dribbles success rate": "Dribble\nSuccess %",
        "Touches": "Touches",
        "Touches in opposition box": "Touches In\nOpp. Box",
        "Fouls won": "Fouls Won",
        "Dispossessed": "Dispossessed"
    },
    "Defending": {
        "Tackles won": "Tackles\nWon",
        "Tackles won %": "Tackles\nWon %",
        "Duels won": "Duels\nWon",
        "Duels won %": "Duels\nWon %",
        "Aerials won": "Aerials\nWon",
        "Aerials won %": "Aerials\nWon %",
        "Interceptions": "Interceptions",
        "Blocked scoring attempt": "Blocks",
        "Fouls committed": "Fouls\nCommitted",
        "Recoveries": "Recoveries",
        "Possession won final 3rd": "Poss. Won\nIn Final 3rd",
        "Dribbled past": "Dribbled\nPast"
    },
    "Goalkeeping": {
        "Saves": "Saves",
        "Save percentage": "Save %",
        "Goals conceded": "Goals\nConceded",
        "Goals prevented": "Goals\nPrevented",
        "Clean sheets": "Clean\nSheets",
        "Penalties faced": "Penalties\nFaced",
        "Penalty goals conceded": "Penalty Goals\nConceded",
        "Penalty saves": "Penalty\nSaves",
        "Error led to goal": "Errors\nLed to Goal",
        "Acted as sweeper": "Sweeper\nActions",
        "High claim": "High\nClaims"
    }
}


# Add a horizontal line
st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# Define the run function
def run():

    # Set up the Streamlit app
    st.markdown("<h1 style='font-size: 24px;'>Radar Comparison</h1>", unsafe_allow_html=True)
    
    
    
    # Player name search input for Player 1
    search_input1 = st.text_input("Enter Player Name for Player 1").strip()
    
    # Filter players based on search input for Player 1
    if search_input1:
        filtered_players1 = df[df['Player Name'].str.contains(search_input1, case=False, na=False)]
        player_names1 = filtered_players1['Player Name'].unique().tolist()
    else:
        player_names1 = []
    
    # Dropdown for selecting player name from the filtered list for Player 1
    player_name1 = st.selectbox("Select Player 1", player_names1) if player_names1 else None
    
    # Player name search input for Player 2
    search_input2 = st.text_input("Enter Player Name for Player 2").strip()
    
    # Filter players based on search input for Player 2
    if search_input2:
        filtered_players2 = df[df['Player Name'].str.contains(search_input2, case=False, na=False)]
        player_names2 = filtered_players2['Player Name'].unique().tolist()
    else:
        player_names2 = []
    
    # Dropdown for selecting player name from the filtered list for Player 2
    player_name2 = st.selectbox("Select Player 2", player_names2) if player_names2 else None
    
    if player_name1 and player_name2:
        # Get player data for both players
        player_data1 = filtered_players1[filtered_players1['Player Name'] == player_name1]
        player_data2 = filtered_players2[filtered_players2['Player Name'] == player_name2]
    
        team_id1 = player_data1.iloc[0]['Team ID']
        team_id2 = player_data2.iloc[0]['Team ID']
        
    
        # Collect metrics for radar chart, ensuring both players have valid values
        valid_metrics = {category: [] for category in available_metrics.keys()}
        
        for category, metrics in available_metrics.items():
            for metric in metrics:
                value1 = player_data1.iloc[0].get(metric)
                value2 = player_data2.iloc[0].get(metric)
        
                # Check for valid metrics for both players
                if pd.notna(value1) and pd.notna(value2):
                    valid_metrics[category].append(metrics[metric])  # Append only if both have valid values
        
        # Dropdowns for each category with multi-select
        selected_metrics = {}
        for category in valid_metrics.keys():
            if valid_metrics[category]:  # Check if there are valid metrics
                selected_metrics[category] = st.multiselect(f"Select metrics for {category}", valid_metrics[category])
    
    
        # Define color mapping for each category
        category_colors = {
            "Shooting": "#e0e0e0",
            "Passing": "#c49c3a",
            "Possession": '#9373d6',
            "Defending": '#4a9697',
            "Goalkeeping": '#7fb26f'
        }
        
        # Prepare the radar chart data using original metric names
        if selected_metrics:
            labels = []
            stats1 = []
            stats2 = []
            categories = []  # To store the category of each selected metric
        
            for category, selected in selected_metrics.items():
                for display_name in selected:
                    # Find the original metric name based on the display name safely
                    original_metric = None
                    for key, value in available_metrics[category].items():
                        if value == display_name:
                            original_metric = key
                            break
                    
                    # Check if the original metric exists in the player data for both players
                    if original_metric and original_metric in player_data1.columns and original_metric in player_data2.columns:
                        value1 = player_data1.iloc[0][original_metric]
                        value2 = player_data2.iloc[0][original_metric]
                        
                        # Ensure both values are valid (non-NaN)
                        if pd.notna(value1) and pd.notna(value2):
                            labels.append(display_name)  # Use the display name for labels
                            stats1.append(value1)
                            stats2.append(value2)
                            categories.append(category)  # Store the category for each metric
        
        # Create radar chart
        num_vars = len(labels)
        
        # Compute angle for each axis, ensuring the first one is at 90 degrees
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        # Rotate angles to start at 90 degrees and then reverse the order for clockwise plotting
        angles = [(angle + np.pi / 2) % (2 * np.pi) for angle in angles]
        angles = angles[::-1]  # Reverse the order for clockwise plotting
        
        # Close the loop by adding the first angle to the end for closing the chart
        angles += angles[:1]  
        stats1 += stats1[:1]  # Close the stats1 loop
        stats2 += stats2[:1]  # Close the stats2 loop
        
        # Create radar chart
        fig1, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        
        # Set background color
        fig1.patch.set_facecolor('#2E2E2A')  # Dark background for the figure
        ax.set_facecolor('#2E2E2A')  # Dark background for the plot area
        
        # Set the color of the outer circle (spines)
        ax.spines['polar'].set_visible(True)  # Ensure the outer circle (spine) is visible
        ax.spines['polar'].set_edgecolor('grey')  # Set the outer circle color to white
        ax.spines['polar'].set_linewidth(1)  # Increase the line width for better visibility
    
        
        # Set y-ticks to be at 20, 40, 60, and 80
        y_ticks = [20, 40, 60, 80]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_ticks, color='grey', size=10)
        ax.set_ylim(0, 100)  # Set the limit of y-axis to 0-100
        ax.yaxis.grid(True, color='grey', linestyle='dashed')
        
        # Plot data
        ax.plot(angles, stats1, color='#1f77b4', linewidth=2, linestyle='solid')
        ax.fill(angles, stats1, color='#1f77b4', alpha=0.25)
        
        ax.plot(angles, stats2, color='#d62728', linewidth=2, linestyle='solid')
        ax.fill(angles, stats2, color='#d62728', alpha=0.25)
        
        # Draw circles at specified intervals (20, 40, 60, 80, and a max circle for 100)
        for tick in [20, 40, 60, 80]:
            circle = plt.Circle((0, 0), tick / 100 * 1.1, color='white', fill=False, linestyle='dotted', linewidth=1.5)
            ax.add_artist(circle)
        
        # Draw the outer circle for the maximum value (100)
        max_circle = plt.Circle((0, 0), 1.1, color='white', fill=False, linestyle='dotted', linewidth=2, zorder=10)
        ax.add_artist(max_circle)
    
    
        
        # Rotate and place each label using the category color
        for angle, label, category in zip(angles[:-1], labels, categories):
            # Calculate rotation
            rotation = angle * 180 / np.pi - 90  # Convert radians to degrees and adjust
            if angle > np.pi:  # Check if the angle is greater than 180 degrees
                rotation += 180  # Flip the rotation by adding 180 degrees
            color = category_colors.get(category, 'white')  # Default to black if category not found
            ax.text(angle, 105, label, ha='center', va='center', rotation=rotation, 
                    rotation_mode='anchor', color=color, fontsize=12, fontproperties=custom_fontt)
        
        # Remove angle labels
        ax.set_xticks([])  # Hides the angle labels
    
        # Extract Minutes Played for both players
        minutes_played1 = player_data1.iloc[0]['Minutes Played']
        minutes_played2 = player_data2.iloc[0]['Minutes Played']
        
        # Title and legend
        ax.text(-0.15, 1.2, "Player Comparison", ha='left', va='center', 
                fontproperties=custom_fontt, fontsize=30, color='white', transform=ax.transAxes)
        
        ax.text(1.065, 1.19, f"{player_name1}\n{int(minutes_played1)} Min.", ha='right', va='center', 
                fontproperties=custom_fontt, fontsize=14, color='#1f77b4', alpha=0.8, transform=ax.transAxes)
        
        ax.text(1.065, 1.1285, f"{player_name2}\n{int(minutes_played2)} Min.", ha='right', va='center', 
                fontproperties=custom_fontt, fontsize=14, color='#d62728', alpha=0.8, transform=ax.transAxes)
        
        ax.text(-0.15, 1.14825, "Each Player's Percentile Rank vs. League's Positional Peers\nOpta Data as of 09/10 | Code by @DanishScout_", 
                ha='left', va='center', fontproperties=custom_font, fontsize=12, color='white', alpha=0.5, transform=ax.transAxes)
    
        # Add a horizontal line at the top
        fig1.add_artist(plt.Line2D((0, 1), (0.935, 0.935), color='white', linewidth=1.5, alpha=0.8, transform=fig1.transFigure))
        
        # Create legend
        legend_elements = []
        for category, color in category_colors.items():
            # Only include categories that have selected metrics
            if category in selected_metrics and selected_metrics[category]:  
                legend_elements.append(plt.Line2D([0], [0], marker='o', color='#2E2E2A', label=category, 
                                                  markerfacecolor=color, markeredgecolor='black', markersize=10))
        
        # Place the legend outside the radar chart
        if legend_elements:  # Only add legend if there are legend elements
            legend = ax.legend(handles=legend_elements, loc='upper right', fontsize=10, frameon=False, 
                               labelspacing=0.5, handletextpad=0.3, framealpha=0.0, bbox_to_anchor=(1.15, 0.075),
                               prop=custom_font)  # Use custom font for legend
        
            # Set the legend text color to white using plt.setp()
            plt.setp(legend.get_texts(), color='white')  # Change legend text color to white
    
    
    
        if player_name1 and player_name2:
            # Get player data for both players
            player_data1 = filtered_players1[filtered_players1['Player Name'] == player_name1]
            player_data2 = filtered_players2[filtered_players2['Player Name'] == player_name2]
        
            # Extract the team IDs for Player 1 and Player 2
            team_id1 = player_data1.iloc[0]['Team ID']
            team_id2 = player_data2.iloc[0]['Team ID']
        
            # URL format for fetching logos
            logo_url1 = f'https://images.fotmob.com/image_resources/logo/teamlogo/{team_id1}.png'
            logo_url2 = f'https://images.fotmob.com/image_resources/logo/teamlogo/{team_id2}.png'
        
            try:
                # Fetch Player 1's team logo
                response1 = requests.get(logo_url1)
                logo1_image = Image.open(BytesIO(response1.content))
                
                # Add axes and place the logo for Player 1 (top right of the radar chart)
                logo_ax1 = fig1.add_axes([0.96, 1.01, 0.034, 0.034])
                logo_ax1.imshow(logo1_image, alpha=1)  # Adjust alpha for transparency
                logo_ax1.axis('off')  # Hide the axis
        
            except Exception as e:
                st.error(f"Error loading team logo for Player 1: {e}")
        
            try:
                # Fetch Player 2's team logo
                response2 = requests.get(logo_url2)
                logo2_image = Image.open(BytesIO(response2.content))
                
                # Add axes and place the logo for Player 2 (just below Player 1's logo)
                logo_ax2 = fig1.add_axes([0.96, 0.9625, 0.033, 0.033])
                logo_ax2.imshow(logo2_image, alpha=1)  # Adjust alpha for transparency
                logo_ax2.axis('off')  # Hide the axis
        
            except Exception as e:
                st.error(f"Error loading team logo for Player 2: {e}")
    
    
    
    
    
    # Button to display the plot
    if st.button("Show Radar Chart"):
        st.pyplot(fig1)

# Finally, call the run function to execute the app
if __name__ == "__main__":
    run()