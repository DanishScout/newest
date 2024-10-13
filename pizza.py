import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import matplotlib.font_manager as fm
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
from matplotlib.patches import Circle

# Font paths
font_path = "Rajdhani-Bold.ttf"
font_pathh = "Alexandria-Regular.ttf"
font_pathhh = "Alexandria-SemiBold.ttf"

# Load the font using FontProperties
custom_font = fm.FontProperties(fname=font_path)
custom_fontt = fm.FontProperties(fname=font_pathh)
custom_fonttt = fm.FontProperties(fname=font_pathhh)

# Load the new CSV files into DataFrames
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

# Combine all DataFrames into one
data = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16], ignore_index=True)

# Filter players with at least 150 minutes played
data = data[data['Minutes Played'] >= 150]

# Filter players based on the specified leagues
valid_leagues = ['Superligaen', 'Allsvenskan', 'Eliteserien', 'Premier League', 'LaLiga',
                 'Bundesliga', 'Serie A', 'Ligue 1', 'Eredivisie', 'Liga Portugal', 'First Division A',
                 'Premiership', 'J. League', 'Liga Profesional', 'Brazilian Serie A', 'Austrian Bundesliga']
data = data[data['League'].isin(valid_leagues)]

# Define a function to fetch the logo
@st.cache_data
def fetch_team_logo(team_id):
    image_url = f"https://images.fotmob.com/image_resources/logo/teamlogo/{team_id}.png"
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        logo = Image.open(BytesIO(response.content))
        return logo
    except Exception as e:
        st.error(f"Error fetching logo: {e}")
        return None

# Define the run function
def run():
    
    # Add your existing title and content
    st.markdown("<h1 style='font-size: 24px;'>Pizza Chart</h1>", unsafe_allow_html=True)
    
    # Player name search input
    search_input = st.text_input("Enter Player Name").strip()
    
    # Filter players based on search input
    if search_input:
        filtered_players = data[data['Player Name'].str.contains(search_input, case=False, na=False)]
        player_names = filtered_players['Player Name'].unique().tolist()
    else:
        player_names = []
    
    # Dropdown for selecting player name from the filtered list
    if player_names:
        player_name = st.selectbox("Select Player", player_names)
    else:
        player_name = None
    
    if player_name:
        player_data = filtered_players[filtered_players['Player Name'] == player_name]
        
        # Get the team ID from player data
        team_id = player_data.iloc[0]['Team ID']
        
        # Fetch team name from the player data directly
        team_name = player_data.iloc[0]['Team Name'] if 'Team Name' in player_data.columns else "Unknown Team"
    
        # Fetch team logo
        team_logo = fetch_team_logo(team_id)
        if team_logo:
            # Extract performance stats
            henrik_row = player_data.iloc[0]
            performance_stats = [(metric, value) for metric, value in zip(henrik_row.index[4:], henrik_row.values[4:])]
    
            # Filter out metrics with "N/A" and NaN
            valid_metrics = [(metric, value) for metric, value in performance_stats if value != "N/A" and pd.notna(value)]
    
            # Available metrics categories
            available_metrics = {
                "Goals": ("Shooting", "Goals"),
                "xG": ("Shooting", "xG"),
                "xG excl. penalty": ("Shooting", "npxG"),
                "xGOT": ("Shooting", "xGOT"),
                "Shots": ("Shooting", "Shots"),
                "Shots on target": ("Shooting", "Shots\nOn target"),
                
                "Assists": ("Passing", "Assists"),
                "xA": ("Passing", "xA"),
                "Chances created": ("Passing", "Key\nPasses"),
                "Accurate passes": ("Passing", "Accurate\nPasses"),
                "Pass accuracy": ("Passing", "Pass\nAccuracy, %"),
                "Accurate long balls": ("Passing", "Accurate\nLong Balls"),
                "Long ball accuracy": ("Passing", "Long Ball\nAccuracy, %"),
                "Successful crosses": ("Passing", "Successful\nCrosses"),
                "Cross accuracy": ("Passing", "Cross\nAccuracy, %"),
                
                "Dribbles": ("Possession", "Completed\nTake-ons"),
                "Dribbles success rate": ("Possession", "Take-on\nSuccess, %"),
                "Touches": ("Possession", "Touches"),
                "Touches in opposition box": ("Possession", "Touches In\nOpp. box"),
                "Fouls won": ("Possession", "Fouls Won"),
                "Dispossessed": ("Possession", "Dispossessed"),
                
                "Tackles won": ("Defending", "Tackles\nWon"),
                "Tackles won %": ("Defending", "Tackles\nWon, %"),
                "Duels won": ("Defending", "Duels Won"),
                "Duels won %": ("Defending", "Duels\nWon, %"),
                "Aerials won": ("Defending", "Aerials\nWon"),
                "Aerials won %": ("Defending", "Aerials\nWon, %"),
                "Interceptions": ("Defending", "Interceptions"),
                "Blocked scoring attempt": ("Defending", "Blocks"),
                "Fouls committed": ("Defending", "Fouls"),
                "Recoveries": ("Defending", "Recoveries"),
                "Possession won final 3rd": ("Defending", "Possession Won\nFinal 3rd"),
                "Dribbled past": ("Defending", "Dribbled\nPast"),
                
                # New Goalkeeping Metrics
                "Saves": ("Goalkeeping", "Saves"),
                "Save percentage": ("Goalkeeping", "Save %"),
                "Goals conceded": ("Goalkeeping", "Goals\nConceded"),
                "Goals prevented": ("Goalkeeping", "Goals\nPrevented"),
                "Clean sheets": ("Goalkeeping", "Clean\nSheets"),
                "Penalties faced": ("Goalkeeping", "Penalties\nFaced"),
                "Penalty goals conceded": ("Goalkeeping", "Penalties\nConceded"),
                "Penalty saves": ("Goalkeeping", "Penalty\nSaves"),
                "Error led to goal": ("Goalkeeping", "Error\nLed To Goal"),
                "Acted as sweeper": ("Goalkeeping", "Sweeper\nActions"),
                "High claim": ("Goalkeeping", "High\nClaims")
            }
    
            # Group metrics by categories for better organization
            shooting_metrics = [m for m in available_metrics if available_metrics[m][0] == "Shooting" and m in dict(valid_metrics)]
            passing_metrics = [m for m in available_metrics if available_metrics[m][0] == "Passing" and m in dict(valid_metrics)]
            possession_metrics = [m for m in available_metrics if available_metrics[m][0] == "Possession" and m in dict(valid_metrics)]
            defending_metrics = [m for m in available_metrics if available_metrics[m][0] == "Defending" and m in dict(valid_metrics)]
            goalkeeping_metrics = [m for m in available_metrics if available_metrics[m][0] == "Goalkeeping" and m in dict(valid_metrics)]
            
            # Create display names mapping
            display_names = {metric: available_metrics[metric][1] for metric in available_metrics}
            
            # Multiselect for users to choose metrics with category grouping
            st.subheader("Select Metrics (at least 8)")
            
            # Allow users to select metrics by category with display names
            selected_shooting = st.multiselect("Shooting Metrics", [display_names[m] for m in shooting_metrics])
            selected_passing = st.multiselect("Passing Metrics", [display_names[m] for m in passing_metrics])
            selected_possession = st.multiselect("Possession Metrics", [display_names[m] for m in possession_metrics])
            selected_defending = st.multiselect("Defending Metrics", [display_names[m] for m in defending_metrics])
            selected_goalkeeping = st.multiselect("Goalkeeping Metrics", [display_names[m] for m in goalkeeping_metrics])
            
            # Combine all selected metrics by their original keys
            def get_original_metrics(selected, category):
                return [m for m in available_metrics if available_metrics[m][1] in selected and available_metrics[m][0] == category]
            
            selected_metrics = (
                get_original_metrics(selected_shooting, "Shooting") +
                get_original_metrics(selected_passing, "Passing") +
                get_original_metrics(selected_possession, "Possession") +
                get_original_metrics(selected_defending, "Defending") +
                get_original_metrics(selected_goalkeeping, "Goalkeeping")
            )
            
            # Ensure at least 8 metrics are selected
            if len(selected_metrics) < 2:
                st.warning("Please select at least 2 metrics to display the chart.")
            else:
                # Extract data for the pizza chart
                values = [henrik_row[m] for m in selected_metrics if m in henrik_row]
                params = [display_names[m] for m in selected_metrics if m in henrik_row]
    
                # Color coding based on category
                slice_colors = []
                for metric in selected_metrics:
                    category = available_metrics[metric][0]
                    if category == "Shooting":
                        slice_colors.append("#1A78CF")  # Blue for shooting
                    elif category == "Passing":
                        slice_colors.append("#FF9300")  # Orange for passing
                    elif category == "Possession":
                        slice_colors.append("#58AC4E")  # Green for possession
                    elif category == "Defending":
                        slice_colors.append("#aa42af")  # Purple for defending
                    elif category == "Goalkeeping":
                        slice_colors.append("pink")  # Pink for goalkeeping
    
                # Submit button to create the pizza chart
                if st.button("Generate Chart"):
                    # Create the pizza chart
                    baker = PyPizza(
                        params=params,                  # list of parameters
                        background_color="#222222",     # background color
                        straight_line_color="#000000",  # color for straight lines
                        straight_line_lw=1,             # linewidth for straight lines
                        last_circle_color="#000000",    # color for last line
                        last_circle_lw=4,               # linewidth for last circle
                        other_circle_lw=0,              # linewidth for other circles
                        inner_circle_size=20            # size of inner circle
                    )
    
                    fig, ax = baker.make_pizza(
                        values,
                        figsize=(9.5, 11),
                        color_blank_space="same",
                        blank_alpha=0.1,
                        slice_colors=slice_colors,
                        kwargs_slices=dict(edgecolor="#000000", zorder=2, linewidth=2),
                        kwargs_params=dict(color="#F2F2F2", fontsize=12, fontproperties=fm.FontProperties(fname="Alexandria-Regular.ttf"), va="center"),
                        kwargs_values=dict(color="#F2F2F2", fontsize=0, alpha=0, fontproperties=fm.FontProperties(fname="Alexandria-Regular.ttf"), zorder=-5)
                    )
                    
                    # Create legend
                    if selected_metrics:  # Check if any metrics are selected
                        category_labels = [available_metrics[metric][0] for metric in selected_metrics]  # Get labels
                        # Create a mapping from metric to its corresponding label and color
                        category_colors = {available_metrics[metric][0]: slice_colors[i] for i, metric in enumerate(selected_metrics)}  
                    
                        # Create a custom legend with unique colors
                        unique_colors = {}
                        handles = []
                    
                        for label in category_labels:
                            color = category_colors[label]
                            if color not in unique_colors:  # Only add unique colors
                                unique_colors[color] = label
                                handles.append(plt.Line2D([0], [0], marker='o', linestyle='None', label=f"{label}", markersize=10, markerfacecolor=color, markeredgecolor='black'))
                    
                        # Add legend to the plot with customized position and no frame, and apply custom font
                        legend = ax.legend(handles=handles, loc='lower right', fontsize=10, 
                                           frameon=False, bbox_to_anchor=(1.125, -0.05), handletextpad=0.5, 
                                           prop=custom_fontt)  # Apply custom font properties here
                        
                        # Set the legend text color to white
                        plt.setp(legend.get_texts(), color='white', alpha=0.7)  # Change legend text color to white
    
                    # Retrieve Minutes Played and Age from the player data
                    position = player_data['Primary Position']  # Assuming 'Age' exists
                
                    fig.text(
                        0.08, 0.9525, f"{player_name}", size=25,
                        ha="left", fontproperties=custom_fontt, color="#F2F2F2"
                    )
                
                    fig.text(
                        0.08, 0.932,
                        "Percentile Rank vs. Positional Peers | Stats per 90",
                        size=10,
                        ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
                    )
                
                    # Convert 'Minutes Played' to an integer to remove decimals
                    minutes_played = int(henrik_row['Minutes Played'])
                    
                    fig.text(
                        0.08, 0.902,
                        f"Minutes Played: {minutes_played} | Age: {henrik_row['Age']} | {henrik_row['League']} | Opta Data\nData as of 26/09 | Code by @DanishScout_",
                        size=10,
                        ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
                    )
                
                    # Add a horizontal line at the top with the team's primary color
                    fig.add_artist(plt.Line2D((0, 1), (0.88, 0.88), color='white', linewidth=1.5, alpha=0.8, transform=fig.transFigure))
                
                    # Coordinates for the logo inside the pizza chart
                    logo_ax = fig.add_axes([0.84, 0.89, 0.1, 0.1])  # [x0, y0, width, height]
                    logo_ax.imshow(team_logo)
                    logo_ax.axis('off')  # Hide the axis for the logo
                
                    # Coordinates for the circles
                    circle1_center_x, circle1_center_y = 0.5, 0.5  # Circle 1 center
                    circle2_center_x, circle2_center_y = 0.5, 0.5  # Circle 2 center
                    circle3_center_x, circle3_center_y = 0.5, 0.5  # Circle 3 center
                    circle4_center_x, circle4_center_y = 0.5, 0.5  # Circle 4 center
                    
                    # Add circles
                    circle_params = [
                        (0.415, circle1_center_x, circle1_center_y),  # Circle 1
                        (0.330, circle2_center_x, circle2_center_y),  # Circle 2
                        (0.245, circle3_center_x, circle3_center_y),  # Circle 3
                        (0.160, circle4_center_x, circle4_center_y)   # Circle 4
                    ]
                    
                    for radius, x, y in circle_params:
                        circle = Circle((x, y), radius, color='black', alpha=0.25, fill=False, zorder=50, linewidth=1.75, transform=ax.transAxes)
                        ax.add_patch(circle)
                    
                    # Add text above circles
                    # Add text '80' above circle 1
                    ax.text(circle1_center_x, circle1_center_y + 0.395, '80',
                            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
                    
                    # Add text '60' above circle 2
                    ax.text(circle2_center_x, circle2_center_y + 0.31, '60',
                            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
                    
                    # Add text '40' above circle 3
                    ax.text(circle3_center_x, circle3_center_y + 0.225, '40',
                            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
                    
                    # Add text '20' above circle 4
                    ax.text(circle4_center_x, circle4_center_y + 0.14, '20',
                            ha='center', va='center', fontsize=13, zorder=80, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
                    
                    # Load the image
                    logo_image = Image.open('scout.png')
                    
                    # Coordinates for the top right corner
                    logo_ax = fig.add_axes([0.4421, 0.427, 0.1375, 0.1375])
                    
                    # Display the image with reduced transparency
                    logo_ax.imshow(logo_image, alpha=0.1)  # Set alpha to 0.1 (adjust as needed)
                    
                    # Hide the axis
                    logo_ax.axis('off')
    
                    # Visualize performance stats in a pizza chart
                    st.pyplot(fig)

# Finally, call the run function to execute the app
if __name__ == "__main__":
    run()