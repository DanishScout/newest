import requests
import pandas as pd
from mplsoccer.pitch import Pitch
from mplsoccer.pitch import VerticalPitch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
from scipy.interpolate import interp1d
import urllib.request
from PIL import Image
import numpy as np
import json
import streamlit as st

# Load the matches.csv file at the start
@st.cache_data
def load_matches():
    return pd.read_csv('matches.csv')

# Load the matches data
matches_data = load_matches()

# Add a horizontal line
st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

# Define the run function
def run():
    
    # Add your existing title and content
    st.markdown("<h1 style='font-size: 24px;'>Match Report</h1>", unsafe_allow_html=True)
    
    # Create dropdown selectors for home and away teams
    home_teams = matches_data['Home Team'].unique()
    away_teams = matches_data['Away Team'].unique()
    
    # Select Home Team
    selected_home_team = st.selectbox("Select Home Team", home_teams)
    
    # Select Away Team
    selected_away_team = st.selectbox("Select Away Team", away_teams)
    
    # Find the corresponding Match ID
    match_id = matches_data.loc[
        (matches_data['Home Team'] == selected_home_team) & 
        (matches_data['Away Team'] == selected_away_team), 
        'Match ID'
    ]
    
    # Check if a match is found
    if not match_id.empty:
        match_id_value = match_id.values[0]  # Get the actual Match ID value
    
        # Example API call using the match ID (modify as needed)
        r = requests.get(f"https://www.fotmob.com/api/matchDetails?matchId={match_id_value}")
    
        # Check if the data fetch was successful
        if r.status_code == 200:
            match_data = r.json()
    
            # Check if the match has started
            if match_data.get("general", {}).get("started"):
                # Continue with your plotting or further logic here
                pass  # Replace with your logic for when the match has started
            else:
                # Show an error message if the match has not started
                st.error("No available data. The match has not started yet.")
                st.stop()  # Stop the code execution here
    
    
    
        # Paths to custom fonts
        font_path = "Rajdhani-Bold.ttf"
        font_pathh = "Alexandria-Regular.ttf"
        font_pathhh = "Alexandria-SemiBold.ttf"
        
        # Load the font using FontProperties
        custom_font = fm.FontProperties(fname=font_path)
        custom_fontt = fm.FontProperties(fname=font_pathh)
        custom_fonttt = fm.FontProperties(fname=font_pathhh)
        
        # Extract team colors
        home_team_colors = match_data.get('general', {}).get('teamColors', {}).get('darkMode', {}).get('home')
        away_team_colors = match_data.get('general', {}).get('teamColors', {}).get('darkMode', {}).get('away')
        
        print("Home Team Colors:", home_team_colors)
        print("Away Team Colors:", away_team_colors)
        
        #############33
        
        import matplotlib.patheffects as path_effects
        from matplotlib.patches import FancyArrowPatch
        
        #Extract stats data
        stats_data = match_data.get('content', {}).get('stats', {}).get('Periods', {}).get('All', {}).get('stats', [])
        titles = [stat.get('title') for stat in stats_data]
        
        
        # Extract shot data
        shots = match_data.get('content', {}).get('shotmap', {}).get('shots', [])
        home_team_id = match_data.get('general', {}).get('homeTeam', {}).get('id')
        away_team_id = match_data.get('general', {}).get('awayTeam', {}).get('id')
        
        # Create DataFrame from shot data
        df = pd.DataFrame(shots)
        
        # Fetch momentum data
        momentum_data = match_data.get('content', {}).get('matchFacts', {}).get('momentum', {}).get('main', {}).get('data', [])
        
        stats_data = match_data.get('content', {}).get('stats', {}).get('Periods', {}).get('All', {}).get('stats', [])
        titles = [stat.get('title') for stat in stats_data]
        
        
        #####################
        
        titles = []
        stats_data = match_data.get('content', {}).get('stats', [])
        for item in stats_data:
            if isinstance(item, dict):
                periods = item.get('Periods', {})
                all_period = periods.get('All', {})
                stats = all_period.get('stats', [])
                for stat in stats:
                    if isinstance(stat, dict) and 'title' in stat:
                        titles.append(stat['title'])
        
        #############
        
        
        
        #######
        
        # Extract titles from stats_data
        titles = []
        
        # Check if 'Periods' key exists
        if 'Periods' in stats_data:
            periods = stats_data['Periods']
        
            # Check if 'All' key exists
            if 'All' in periods:
                all_period = periods['All']
        
                # Check if 'stats' key exists
                if 'stats' in all_period:
                    stats = all_period['stats']
        
                    # Iterate over each item in 'stats'
                    for item in stats:
                        # Check if 'stats' key exists in the current item
                        if 'stats' in item:
                            inner_stats = item['stats']
        
                            # Iterate over each inner item in 'stats'
                            for inner_item in inner_stats:
                                # Check if 'title' key exists in the current inner item
                                if 'title' in inner_item:
                                    # Append the title to the list of titles
                                    titles.append(inner_item['title'])
        
        
        
        ###############
        
        # Extract titles and values from stats_data
        stats_dict = {}
        
        # Check if 'Periods' key exists
        if 'Periods' in stats_data:
            periods = stats_data['Periods']
        
            # Check if 'All' key exists
            if 'All' in periods:
                all_period = periods['All']
        
                # Check if 'stats' key exists
                if 'stats' in all_period:
                    stats = all_period['stats']
        
                    # Iterate over each item in 'stats'
                    for item in stats:
                        # Check if 'stats' key exists in the current item
                        if 'stats' in item:
                            inner_stats = item['stats']
        
                            # Iterate over each inner item in 'stats'
                            for inner_item in inner_stats:
                                # Check if both 'title' and 'stats' keys exist in the current inner item
                                if 'title' in inner_item and 'stats' in inner_item:
                                    # Extract the title and corresponding stats
                                    title = inner_item['title']
                                    stats_values = inner_item['stats']
        
                                    # Store the title and stats values in the stats_dict
                                    stats_dict[title] = stats_values
        
        
        ###############
        
        # Create a pitch
        pitch = Pitch(pitch_type='uefa', pitch_color='#2E2E2A', line_color='#616A67')
        
        # Increase figure size
        fig2, ax = pitch.draw(figsize=(10, 8))
        
        # Plot shots
        for index, row in df.iterrows():
            xG = row['expectedGoals']
            xGot = row['expectedGoalsOnTarget']
            if pd.notnull(xG):  # Check if xG value is not null
                if row['eventType'] == 'Goal':
                    if row['shotType'] == 'own':
                        marker = 's'  # Square marker for own goals
                    else:
                        marker = 'o'  # Circle marker for regular goals
                    color = '#47B745'
                    edgecolor = 'black'
                    zorder = 3
                elif xGot > 0:
                    color = '#C8C329'
                    edgecolor = 'black'
                    zorder = 2
                    marker = 'o'  # Circle marker for shots on target
                else:
                    color = '#C82929'
                    edgecolor = 'black'
                    zorder = 1
                    marker = 'o'  # Circle marker for other shots
        
                # Determine if the shot belongs to the home team or the away team
                if row['teamId'] == home_team_id:
                    x_coordinate = 105 - row['x']  # Flip x-coordinate for home team shots
                    y_coordinate = 68 - row['y']  # Flip y-coordinate for home team shots
                else:
                    x_coordinate = row['x']  # Keep x-coordinate unchanged for away team shots
                    y_coordinate = row['y']  # Keep y-coordinate unchanged for away team shots
        
                ax.scatter(x_coordinate, y_coordinate, linewidth=1.5, color=color, edgecolor=edgecolor,
                           s=xG * 900, alpha=0.8, zorder=zorder, label=f"{row['teamId']} Shots", marker=marker)
            else:
                # Handle case where xG value is null (e.g., own goal)
                # Mark the location with a red square marker
                if row['teamId'] == home_team_id:
                    x_coordinate = 105 - row['x']  # Flip x-coordinate for home team shots
                    y_coordinate = 68 - row['y']  # Flip y-coordinate for home team shots
                else:
                    x_coordinate = row['x']  # Keep x-coordinate unchanged for away team shots
                    y_coordinate = row['y']  # Keep y-coordinate unchanged for away team shots
        
                ax.scatter(x_coordinate, y_coordinate, linewidth=2, color='#BD1A64', edgecolor='black', s=150,
                           alpha=0.8, zorder=3, marker='X')
        
        # Extract team colors
        home_team_colors = match_data.get('general', {}).get('teamColors', {}).get('darkMode', {}).get('home')
        away_team_colors = match_data.get('general', {}).get('teamColors', {}).get('darkMode', {}).get('away')
        
        print("Home Team Colors:", home_team_colors)
        print("Away Team Colors:", away_team_colors)
        
        
        # Filter out entries for minutes 45.5 and 90.5 from momentum data
        momentum_data_filtered = [moment for moment in momentum_data if moment['minute'] not in [45.5, 90.5]]
        
        # Plot momentum
        if momentum_data_filtered:
            minute_values = [moment['minute'] for moment in momentum_data_filtered]
            momentum_values = [moment['value'] for moment in momentum_data_filtered]
        
            # Interpolate momentum data
            interp_func = interp1d(minute_values, momentum_values, kind='linear')
        
            # Define x values for interpolation
            x_interp = range(min(minute_values), int(max(minute_values)) + 1)
        
            # Scale factor for momentum visualization
            momentum_scale_factor = 30
        
            # Add an offset of 6.5 to the x values for momentum visualization
            x_offset = 6.5
        
            # Plot bars for momentum at every minute
            for minute, momentum in zip(minute_values, momentum_values):
                # Determine the color based on momentum direction
                if momentum >= 0:
                    bar_color = home_team_colors
                    bar_height = momentum / momentum_scale_factor
                    y_coord = 0
                else:
                    bar_color = away_team_colors
                    bar_height = abs(momentum) / momentum_scale_factor
                    y_coord = -bar_height  # Adjust y-coordinate for the away team
        
                # Plot the bar with black edge color
                ax.bar(minute + x_offset, bar_height, color=bar_color, width=1, alpha=1, bottom=y_coord, edgecolor='black', zorder=20)
        
            # Set y-limits to ensure bars fit between the two lines
            ax.set_ylim(-10, 10)
        
            # Add a horizontal line at y-coordinate -10
            ax.hlines(y=-3.475, xmin=0 + x_offset, xmax=91 + x_offset, color='white', linewidth=1, alpha=0.6)
        
            # Add a horizontal line at y-coordinate +10
            ax.hlines(y=3.475, xmin=0 + x_offset, xmax=91 + x_offset, color='white', linewidth=1, alpha=0.6)
        
            # Add the text 'Momentum' centrally below the line
            ax.text(13.25, 5.5, 'Momentum', color='white', fontsize=14, ha='center', va='center', fontproperties=custom_fonttt, alpha=0.7)
            ax.text(0 + x_offset, -6.75, "1'", color='white', fontsize=14, ha='center', va='center', fontproperties=custom_fonttt, alpha=0.7)
            ax.text(46.75 + x_offset, -6.75, "46'", color='white', fontsize=14, ha='center', va='center', fontproperties=custom_fonttt, alpha=0.7)
            ax.text(91 + x_offset, -6.75, "90'", color='white', fontsize=14, ha='center', va='center', fontproperties=custom_fonttt, alpha=0.7)
        
        
        # Set figure face color
        fig2.set_facecolor('#2E2E2A')
        
        # Set the y-axis limit to create space below the momentum visualization
        ax.set_ylim(bottom=-8)
        ax.set_ylim(top=75)
        
        # Define common fontsize and fontproperties
        common_fontsize = 20
        common_fontproperties = custom_font
        
        # Define colors based on value comparison
        def color_by_magnitude(value1, value2):
            if value1 > value2:
                return '#7DC148', '#F05E5E'
            elif value1 < value2:
                return '#F05E5E', '#7DC148'
            else:
                return 'white', 'white'
        
        # Define the text effect
        text_effect = [path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()]
        
        # Extract ball possession data
        ball_possession_home = stats_dict['Ball possession'][0]
        ball_possession_away = stats_dict['Ball possession'][1]
        
        # Determine colors for ball possession values
        possession_color_home, possession_color_away = color_by_magnitude(ball_possession_home, ball_possession_away)
        
        # Add text annotations for ball possession values with colors and text effect
        ax.text(40, 51, f'{ball_possession_home}%', color=possession_color_home, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        ax.text(65, 51, f'{ball_possession_away}%', color=possession_color_away, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        
        # Extract accurate passes data
        accurate_passes_home = stats_dict['Accurate passes'][0]
        accurate_passes_away = stats_dict['Accurate passes'][1]
        
        # Extract the first three digits of the accurate passes values
        accurate_passes_home_formatted = accurate_passes_home.split(' ')[0][:3]
        accurate_passes_away_formatted = accurate_passes_away.split(' ')[0][:3]
        
        # Determine colors for accurate passes values
        passes_color_home, passes_color_away = color_by_magnitude(accurate_passes_home_formatted, accurate_passes_away_formatted)
        
        # Add text annotations for accurate passes values with colors and text effect
        ax.text(40, 43, f'{accurate_passes_home_formatted}', color=passes_color_home, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        ax.text(65, 43, f'{accurate_passes_away_formatted}', color=passes_color_away, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        
        
        # Extract big chances data
        box_home = stats_dict['Big chances'][0]
        box_away = stats_dict['Big chances'][1]
        
        # Determine colors for big chances values
        chances_color_home, chances_color_away = color_by_magnitude(box_home, box_away)
        
        # Add text annotations for big chances values with colors and text effect
        ax.text(40, 35, f'{box_home}', color=chances_color_home, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        ax.text(65, 35, f'{box_away}', color=chances_color_away, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        
        # Extract expected goals (xG) data
        xG_home = stats_dict['Expected goals (xG)'][0]
        xG_away = stats_dict['Expected goals (xG)'][1]
        
        # Determine colors for xG values
        xG_color_home, xG_color_away = color_by_magnitude(xG_home, xG_away)
        
        # Add text annotations for xG values with colors and text effect
        ax.text(40, 27, f'{xG_home}', color=xG_color_home, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        ax.text(65, 27, f'{xG_away}', color=xG_color_away, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        
        
        # Extract xG on target (xGOT) data
        xGOT_home = stats_dict['xG on target (xGOT)'][0]
        xGOT_away = stats_dict['xG on target (xGOT)'][1]
        
        # Determine colors for xG on target (xGOT) values
        xGOT_color_home, xGOT_color_away = color_by_magnitude(xGOT_home, xGOT_away)
        
        # Add text annotations for xG on target (xGOT) values with colors and text effect
        ax.text(40, 19, f'{xGOT_home}', color=xGOT_color_home, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        ax.text(65, 19, f'{xGOT_away}', color=xGOT_color_away, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        
        # Extract total shots data
        total_shots_home = stats_dict['Total shots'][0]
        total_shots_away = stats_dict['Total shots'][1]
        
        # Determine colors for total shots values
        shots_color_home, shots_color_away = color_by_magnitude(total_shots_home, total_shots_away)
        
        # Add text annotations for total shots values with colors and text effect
        ax.text(40, 11, f'{total_shots_home}', color=shots_color_home, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        ax.text(65, 11, f'{total_shots_away}', color=shots_color_away, ha='center', fontsize=common_fontsize, fontproperties=common_fontproperties, path_effects=text_effect)
        
        
        
        # Define custom display names for the stats
        stat_titles = ['Ball possession', 'Accurate passes', 'Big chances', 'Expected goals (xG)',
                       'xG on target (xGOT)', 'Total shots']
        
        # Replace the display names as needed
        custom_display_names = ['Possession', 'Passes', 'Big chances', 'xG',
                                'xGOT', 'Shots']
        
        # Define y positions for the stat titles with a -5 difference between each
        y_positions = [52, 52, 52, 52, 52, 52, 52, 52]
        y_positions = [pos - 8 * i for i, pos in enumerate(y_positions)]
        
        # Add stat titles with bounding box and custom display names
        for title, custom_name, y_pos in zip(stat_titles, custom_display_names, y_positions):
            ax.text(52.5, y_pos, custom_name, color='white', fontproperties=custom_fontt,  fontsize=15, ha='center', va='center',
                    bbox=dict(boxstyle="Round", pad=0.3, edgecolor='white', lw=1.5, facecolor='#222525', alpha=0.8, zorder=10))
        
        # Plot relevant metrics in the middle of the pitch with background
        middle_x = 52.5  # Middle of the pitch along x-axis
        middle_y = 52    # Middle of the pitch along y-axis
        
        
        # Add legends manually
        ax.scatter(2, 73, color='#47B745', linewidth=1.5, edgecolors='black', s=150, zorder=5, alpha=0.8, marker='o')
        ax.text(4, 73, 'Goal', color='white', fontsize=12, alpha=0.8, ha='left', va='center', fontproperties=custom_fonttt)
        
        ax.scatter(17, 73, color='#C8C329', linewidth=1.5, edgecolors='black', s=150, zorder=5, alpha=0.8, marker='o')
        ax.text(19, 73, 'On Target', color='white', fontsize=12, alpha=0.8, ha='left', va='center', fontproperties=custom_fonttt)
        
        ax.scatter(17, 70, color='#C82929', linewidth=1.5, edgecolors='black', s=150, zorder=5, alpha=0.8, marker='o')
        ax.text(19, 70, 'Off Target', color='white', fontsize=12, alpha=0.8, ha='left', va='center', fontproperties=custom_fonttt)
        
        ax.scatter(2, 70, color='#BD1A64', linewidth=1.5, edgecolors='black', s=150, zorder=5, alpha=0.8, marker='X')
        ax.text(4, 70, 'Own Goal', color='white', fontsize=12, alpha=0.8, ha='left', va='center', fontproperties=custom_fonttt)
        
        # Add circles with white edge color for xG values 0.2, 0.6, and 1.0
        circle_positions_right = [(84.5, 71.5), (88.3, 71.5), (93, 71.5)]  # x, y positions of circles on the right side
        xG_values_right = [0.2, 0.5, 0.8]  # xG values corresponding to each circle
        
        for pos, xG in zip(circle_positions_right, xG_values_right):
            ax.scatter(pos[0], pos[1], color='none', linewidth=2, edgecolors='white', s=xG * 800, zorder=5, alpha=0.8)
        
        # Add text annotations for 'Low xG' and 'High xG'
        ax.text(82.5, 71.5, 'Low xG', color='white', alpha=0.8, fontsize=13, ha='right', va='center', fontproperties=custom_fonttt)
        ax.text(96, 71.5, 'High xG', color='white', alpha=0.8, fontsize=13, ha='left', va='center', fontproperties=custom_fonttt)
        
        
        
        # Fetch team logos from URLs within the header and teams keys
        home_team_logo_url = None
        away_team_logo_url = None
        
        teams_data = match_data.get('header', {}).get('teams', [])
        for team in teams_data:
            if 'imageUrl' in team:
                if team.get('id') == home_team_id:
                    home_team_logo_url = team['imageUrl']
                elif team.get('id') == away_team_id:
                    away_team_logo_url = team['imageUrl']
        
        print("Home Team Logo URL:", home_team_logo_url)
        print("Away Team Logo URL:", away_team_logo_url)
        
        # Define a function to load an image from a URL and convert it to a numpy array
        def load_image_from_url(url):
            with urllib.request.urlopen(url) as response:
                image = Image.open(response)
                # Convert the image to RGBA mode with a transparent background
                image = image.convert("RGBA")
                # Replace the yellow background with transparency
                data = np.array(image)
                red, green, blue, alpha = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
                # Set the pixels with yellow background to be fully transparent
                mask = (red > 250) & (green > 250) & (blue < 5)  # Yellow background
                data[:, :, 3][mask] = 0  # Set alpha channel to 0 for yellow background
                image = Image.fromarray(data)
                return np.array(image)
        
        # Load team logos with transparent background
        home_team_logo = load_image_from_url(home_team_logo_url)
        away_team_logo = load_image_from_url(away_team_logo_url)
        
        # Define logo positions
        home_team_logo_pos = [middle_x - 16, middle_y + 6]
        away_team_logo_pos = [middle_x + 9, middle_y + 6]
        
        # Plot team logos
        ax.imshow(home_team_logo, extent=[home_team_logo_pos[0], home_team_logo_pos[0] + 6.5, home_team_logo_pos[1], home_team_logo_pos[1] + 6.5])
        ax.imshow(away_team_logo, extent=[away_team_logo_pos[0], away_team_logo_pos[0] + 6.5, away_team_logo_pos[1], away_team_logo_pos[1] + 6.5])
        
        # Define the color for the lines below logos
        home_line_color = home_team_colors
        away_line_color = away_team_colors
        
        # Add lines below the logos
        ax.plot([40 - 3, 52.825], [57, 57], color=home_line_color, linewidth=5)
        ax.plot([52.825, 65 + 3], [57, 57], color=away_line_color, linewidth=5)
        
        # Extract shot data
        shots = match_data.get('content', {}).get('shotmap', {}).get('shots', [])
        
        # Define the path to the image 'kvaps.png'
        kvaps_image_path = 'mål.png'
        
        # Plot goals on the horizontal line using team logos and 'kvaps.png'
        for shot in shots:
            if shot.get('eventType') == 'Goal':
                # Determine if the goal was an own goal
                is_own_goal = shot.get('isOwnGoal', False)
        
                # Extract the team ID
                team_id = shot.get('teamId')
        
                # Extract the minute of the goal
                minute = shot.get('min')
        
                # Plot goals on the horizontal line using team logos and 'kvaps.png'
        for shot in shots:
            if shot.get('eventType') == 'Goal':
                # Determine if the goal was an own goal
                is_own_goal = shot.get('isOwnGoal', False)
        
                # Extract the team ID
                team_id = shot.get('teamId')
        
                # Extract the minute of the goal
                minute = shot.get('min')
        
                # Set the y-coordinate based on the team (5.5 for home goals, -5.5 for away goals, 5.5 for own goals)
                y_coord = 2.475 if team_id == home_team_id or is_own_goal else -4.475
        
        
                # Plot the 'kvaps.png' image at the specified y-coordinate
                kvaps_image = plt.imread(kvaps_image_path)
                ax.imshow(kvaps_image, extent=[minute + 5.75, minute + 5.75 + 1.8, y_coord, y_coord + 1.8], zorder=25)
        
        
        # Define the arrow properties
        arrow_width = 1
        arrow_length = 10
        
        # Create a double-ended arrow patch
        arrow = FancyArrowPatch((52.5, 70.4), (65, 70.4), arrowstyle='->', color=away_team_colors, lw=2.5, mutation_scale=15)
        
        # Add the arrow to the plot
        ax.add_patch(arrow)
        
        # Define the arrow properties
        arrow_width = 1
        arrow_length = 10
        
        # Create a double-ended arrow patch
        arrow1 = FancyArrowPatch((40, 70.4), (52.5, 70.4), arrowstyle='<-', color=home_team_colors, lw=2.5, mutation_scale=15)
        
        #  Add the arrow to the plot
        ax.add_patch(arrow1)
    
        # Add text annotations for attacking direction
        ax.text(52.5, 71.25, 'Attacking direction', color='white', fontsize=12, ha='center', va='bottom', fontproperties=custom_fonttt, alpha=0.8)
    
        # Extract team names and scores
        home_team_name = None
        away_team_name = None
        home_team_score = None
        away_team_score = None
        
        teams_data = match_data.get('header', {}).get('teams', [])
        for team in teams_data:
            if 'name' in team:
                if team.get('id') == home_team_id:
                    home_team_name = team['name']
                    home_team_score = team['score']
                elif team.get('id') == away_team_id:
                    away_team_name = team['name']
                    away_team_score = team['score']
                
    
        # Format the custom title
        custom_title = f'{home_team_name}  {home_team_score} - {away_team_score}  {away_team_name}'
        
        # Add a custom title
        fig2.text(0.5, 1.02, custom_title, fontproperties=custom_fonttt, fontsize=28, color='white', ha='center')
        
        # Extract league name and round
        league_name = match_data.get('general', {}).get('parentLeagueName', 'Unknown League')
        round_name = match_data.get('general', {}).get('leagueRoundName', 'Unknown Round')
        
        # Format the suptitle
        suptitle_text = f"{league_name}, {round_name} | Opta Data | @DanishScout_"
        
        # Add the suptitle
        fig2.text(0.5, 0.987, suptitle_text, fontproperties=custom_fonttt, fontsize=11, color='white', ha='center', alpha=0.5)
    
        # Add horizontal line at the top
        fig2.add_artist(plt.Line2D((0, 1), (0.95, 0.95), color='white', linewidth=1.5, alpha=0.5, transform=fig2.transFigure))
    
    
    
        # Display the plot in Streamlit
    if st.button("Show Match Report"):
        st.pyplot(fig2)

# Finally, call the run function to execute the app
if __name__ == "__main__":
    run()