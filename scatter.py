import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.font_manager as fm  # Import font manager

# Font path
font_path = "Alexandria-Regular.ttf"
font_pathh = "Alexandria-SemiBold.ttf"
font_pathhh = "Rajdhani-Bold.ttf"
font_pathhhh = "Rajdhani-SemiBold.ttf"

# Load the font using FontProperties
custom_font = fm.FontProperties(fname=font_path)
custom_fontt = fm.FontProperties(fname=font_pathh)
custom_fonttt = fm.FontProperties(fname=font_pathhh)
custom_fontttt = fm.FontProperties(fname=font_pathhhh)

# Load the league tables
league_tables = pd.read_csv('league_tables.csv')

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

# Define the run function
def run():

    # Combine the dataframes
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16], ignore_index=True)
    
    # Filter players with at least 150 minutes played
    df = df[df['Minutes Played'] >= 150]
    
    # Filter players based on the specified leagues
    valid_leagues = ['Superligaen', 'Allsvenskan', 'Eliteserien', 'Premier League', 'LaLiga',
                     'Bundesliga', 'Serie A', 'Ligue 1', 'Eredivisie', 'Liga Portugal', 'First Division A',
                     'Premiership', 'J. League', 'Liga Profesional', 'Brazilian Serie A', 'Austrian Bundesliga']
    df = df[df['League'].isin(valid_leagues)]
    
    # Calculate new metrics: xG + xA per90 and Goals + Assists per90
    df['xG + xA per90'] = df['xG per90'] + df['xA per90']
    df['Goals + Assists per90'] = df['Goals per90'] + df['Assists per90']
    
    # Updated list of available metrics with new metrics added
    available_metrics = [
        # Shooting
        "Goals per90",
        "xG per90",
        "xG excl. penalty per90",
        "xGOT per90",
        "Shots per90",
        "Shots on target per90",
    
        # Passing
        "Assists per90",
        "xA per90",
        "Chances created per90",
        "Accurate passes per90",
        "Pass accuracy per90",
        "Accurate long balls per90",
        "Long ball accuracy per90",
        "Successful crosses per90",
        "Cross accuracy per90",
    
        # Possession
        "Dribbles per90",
        "Dribbles success rate per90",
        "Touches per90",
        "Touches in opposition box per90",
        "Fouls won per90",
        "Dispossessed per90",
    
        # Defending
        "Tackles won per90",
        "Tackles won % per90",
        "Duels won per90",
        "Duels won % per90",
        "Aerials won per90",
        "Aerials won % per90",
        "Interceptions per90",
        "Blocked scoring attempt per90",
        "Fouls committed per90",
        "Recoveries per90",
        "Possession won final 3rd per90",
        "Dribbled past per90",
    
        # Goalkeeping
        "Saves per90",
        "Save percentage % per90",
        "Goals conceded per90",
        "Goals prevented per90",
        "Clean sheets per90",
        "Penalties faced per90",
        "Penalty goals conceded per90",
        "Penalty saves per90",
        "Errors led to goal per90",
        "Sweeper actions per90",
        "High claims per90",
    
        # Newly calculated metrics
        "xG + xA per90",
        "Goals + Assists per90"
    ]
    
    # Custom title mapping for metrics
    custom_titles = {
        "Goals per90": "Goals",
        "xG per90": "xG",
        "xG excl. penalty per90": "npxG",
        "xGOT per90": "xGOT",
        "Shots per90": "Shots",
        "Shots on target per90": "Shots On Target",
        "xG + xA per90": "xG + xA",
        "Goals + Assists per90": "Goals + Assists",
    
        "Assists per90": "Assists",
        "xA per90": "xA",
        "Chances created per90": "Chances\nCreated",
        "Accurate passes per90": "Accurate Passes",
        "Pass accuracy per90": "Pass Accuracy %",
        "Accurate long balls per90": "Accurate Long Balls",
        "Long ball accuracy per90": "Long Ball Accuracy %",
        "Successful crosses per90": "Successful Crosses",
        "Cross accuracy per90": "Cross Accuracy %",
    
        "Dribbles per90": "Successful Dribbles",
        "Dribbles success rate per90": "Dribble Success %",
        "Touches per90": "Touches",
        "Touches in opposition box per90": "Touches in Opp. Box",
        "Fouls won per90": "Fouls Won",
        "Dispossessed per90": "Dispossessed",
    
        "Tackles won per90": "Tackles Won",
        "Tackles won % per90": "Tackles Won %",
        "Duels won per90": "Duels Won",
        "Duels won % per90": "Duels Won %",
        "Aerials won per90": "Aerials Won",
        "Aerials won % per90": "Aerials Won %",
        "Interceptions per90": "Interceptions",
        "Blocked scoring attempt per90": "Blocks",
        "Fouls committed per90": "Fouls Committed",
        "Recoveries per90": "Recoveries",
        "Possession won final 3rd per90": "Poss. Won In Final 3rd",
        "Dribbled past per90": "Dribbled Past",
    
        "Saves per90": "Saves",
        "Save percentage % per90": "Save %",
        "Goals conceded per90": "Goals Conceded",
        "Goals prevented per90": "Goals Prevented",
        "Clean sheets per90": "Clean Sheets",
        "Penalties faced per90": "Penalties Faced",
        "Penalty goals conceded per90": "Penalty Goals Conceded",
        "Penalty saves per90": "Penalty Saves",
        "Errors led to goal per90": "Errors Leading to Goals",
        "Sweeper actions per90": "Sweeper Actions",
        "High claims per90": "High Claims",
    
    }

    
    # Set up the Streamlit app
    st.markdown("<h1 style='font-size: 24px;'>Scatter Plot</h1>", unsafe_allow_html=True)
    
    
    # Define the custom order of positions
    custom_position_order = [
        'Striker', 
        'Right Winger', 
        'Left Winger', 
        'Left Midfielder', 
        'Right Midfielder', 
        'Attacking Midfielder', 
        'Central Midfielder', 
        'Defensive Midfielder', 
        'Left Wing-Back', 
        'Right Wing-Back', 
        'Right Back', 
        'Left Back', 
        'Center Back', 
        'Goalkeeper'
    ]
    
    # Get unique primary positions and sort them based on the custom order
    primary_positions = df['Primary Position'].unique()
    sorted_positions = sorted(primary_positions, key=lambda x: custom_position_order.index(x) if x in custom_position_order else len(custom_position_order))
    
    # Add 'All' option at the beginning of the sorted positions list
    sorted_positions = sorted_positions
    
    # Multi-select for selecting Primary Position
    selected_positions = st.multiselect("Select Primary Positions", sorted_positions)
    
    # Multi-select for selecting League
    selected_leagues = st.multiselect("Select Leagues", valid_leagues)
    
    # Multi-select for selecting Team Ranking
    selected_team_rank = st.selectbox("Select Team Ranking", 
                                        ['All Teams', '>75% (Title Contender)', '>50% (Top Half)', '<50% (Bottom Half)', '<25% (Relegation Candidate)'])
    
    # Sliders for Age and Minutes Played
    age_range = st.slider("Select Age Range", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), 
                          value=(int(df['Age'].min()), int(df['Age'].max())))
    
    minutes_range = st.slider("Select Minutes Played Range", min_value=150, 
                               max_value=int(df['Minutes Played'].max()), 
                               value=(150, int(df['Minutes Played'].max())))
    
    # Filter dataframe based on the selected options
    if 'All' not in selected_positions:
        df = df[df['Primary Position'].isin(selected_positions)]
    
    if 'All' not in selected_leagues:
        df = df[df['League'].isin(selected_leagues)]
    
    df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    df = df[(df['Minutes Played'] >= minutes_range[0]) & (df['Minutes Played'] <= minutes_range[1])]
    
    # Add filtering for team ranking
    if selected_team_rank == '>75% (Title Contender)':
        top_teams = league_tables[league_tables['Ranking'] > 75]['Team ID']
        df = df[df['Team ID'].isin(top_teams)]
    elif selected_team_rank == '>50% (Top Half)':
        bottom_teams = league_tables[league_tables['Ranking'] > 50]['Team ID']
        df = df[df['Team ID'].isin(bottom_teams)]
    elif selected_team_rank == '<50% (Bottom Half)':
        above_75_teams = league_tables[league_tables['Ranking'] <= 50]['Team ID']
        df = df[df['Team ID'].isin(above_75_teams)]
    elif selected_team_rank == '<25% (Relegation Candidate)':
        below_25_teams = league_tables[league_tables['Ranking'] < 25]['Team ID']
        df = df[df['Team ID'].isin(below_25_teams)]
    
    
    # Create a reverse mapping of custom_titles to access original metric names
    reverse_custom_titles = {v: k for k, v in custom_titles.items()}
    
    # Dropdown for selecting the x-axis metric
    x_metric_display = st.selectbox(
        "Select Metric for X-Axis", 
        list(custom_titles.values()),  # Use the values for the dropdown
        index=0
    )
    x_metric = reverse_custom_titles[x_metric_display]  # Get the corresponding original metric name
    
    # Dropdown for selecting the y-axis metric, excluding the selected x_metric
    y_metric_display = st.selectbox(
        "Select Metric for Y-Axis", 
        [title for title in custom_titles.values() if title != x_metric_display],  # Exclude the selected x_metric
        index=0
    )
    y_metric = reverse_custom_titles[y_metric_display]  # Get the corresponding original metric name
    
    
    
    
    
    
    # Use custom titles if available, otherwise fall back to the original metric names
    x_custom_title = custom_titles.get(x_metric, x_metric)
    y_custom_title = custom_titles.get(y_metric, y_metric)
    
    # Sliders for selecting minimum percentiles for annotation with custom titles
    x_percentile = st.slider(f"Min. Percentile Rank for {x_custom_title} to Display Name", min_value=0, max_value=100, value=95)
    y_percentile = st.slider(f"Min. Percentile Rank for {y_custom_title} to Display Name", min_value=0, max_value=100, value=95)
    both_percentile = st.slider(f"Min. Percentile Rank for both {x_custom_title} & {y_custom_title} to Display Name", min_value=0, max_value=100, value=95)
    
    
    # Create scatter plot if both metrics are selected
    if x_metric and y_metric:
        # Prepare data for plotting
        x_data = df[x_metric]
        y_data = df[y_metric]
    
        # Calculate percentiles for both x_metric and y_metric
        # Invert the rank for specified metrics
        inverted_metrics = [
            "Goals conceded per90",
            "Dispossessed per90",
            "Dribbled past per90",
            "Penalty goals conceded per90",
            "Errors led to goal per90"
        ]
    
        # Calculate x_percentile
        if x_metric in inverted_metrics:
            df['x_percentile'] = (1 - df[x_metric].rank(pct=True)) * 100
        else:
            df['x_percentile'] = df[x_metric].rank(pct=True) * 100
        
        # Calculate y_percentile
        if y_metric in inverted_metrics:
            df['y_percentile'] = (1 - df[y_metric].rank(pct=True)) * 100
        else:
            df['y_percentile'] = df[y_metric].rank(pct=True) * 100
    
        # Filter players based on the selected percentiles
        top_x_players = df[df['x_percentile'] >= x_percentile]
        top_y_players = df[df['y_percentile'] >= y_percentile]
        top_both_players = df[(df['x_percentile'] >= both_percentile) & (df['y_percentile'] >= both_percentile)]
    
        # Combine the three sets of players, ensuring unique entries
        top_players = pd.concat([top_x_players, top_y_players, top_both_players]).drop_duplicates()
    
        # Remove NaN values for the plot
        valid_data = df.dropna(subset=[x_metric, y_metric])
    
        # Custom title mapping for metrics
        custom_titles = {
            "Goals per90": "Goals",
            "xG per90": "xG",
            "xG excl. penalty per90": "npxG",
            "xGOT per90": "xGOT",
            "Shots per90": "Shots",
            "Shots on target per90": "Shots on Target",
            "xG + xA per90": "xG + xA",
            "Goals + Assists per90": "Goals + Assists",
            
            "Assists per90": "Assists",
            "xA per90": "xA",
            "Chances created per90": "Chances Created",
            "Accurate passes per90": "Accurate Passes",
            "Pass accuracy per90": "Pass Accuracy %",
            "Accurate long balls per90": "Accurate Long Balls",
            "Long ball accuracy per90": "Long Ball Accuracy %",
            "Successful crosses per90": "Successful Crosses",
            "Cross accuracy per90": "Cross Accuracy %",
            
            "Dribbles per90": "Dribbles",
            "Dribbles success rate per90": "Dribble Success %",
            "Touches per90": "Touches",
            "Touches in opposition box per90": "Touches in Opp. Box",
            "Fouls won per90": "Fouls Won",
            "Dispossessed per90": "Dispossessed",
            
            "Tackles won per90": "Tackles Won",
            "Tackles won % per90": "Tackles Won %",
            "Duels won per90": "Duels Won",
            "Duels won % per90": "Duels Won %",
            "Aerials won per90": "Aerials Won",
            "Aerials won % per90": "Aerials Won %",
            "Interceptions per90": "Interceptions",
            "Blocked scoring attempt per90": "Blocks",
            "Fouls committed per90": "Fouls Committed",
            "Recoveries per90": "Recoveries",
            "Possession won final 3rd per90": "Possession Won In Final 3rd",
            "Dribbled past per90": "Dribbled Past",
            
            "Saves per90": "Saves",
            "Save percentage % per90": "Save %",
            "Goals conceded per90": "Goals Conceded",
            "Goals prevented per90": "Goals Prevented",
            "Clean sheets per90": "Clean Sheets",
            "Penalties faced per90": "Penalties Faced",
            "Penalty goals conceded per90": "Penalty Goals Conceded",
            "Penalty saves per90": "Penalty Saves",
            "Errors led to goal per90": "Errors Leading to Goals",
            "Sweeper actions per90": "Sweeper Actions",
            "High claims per90": "High Claims",
            
        }
    
    
        # Create scatter plot
        plt.figure(figsize=(14, 8), facecolor='#2E2E2A')  # Set the figure facecolor
    
        # Create the axes with a specified facecolor
        ax = plt.subplot()
        ax.set_facecolor('#2E2E2A')  # Set the axes facecolor
    
        # Set the spines color to match the facecolor
        ax.spines['top'].set_color('#2E2E2A')
        ax.spines['right'].set_color('#2E2E2A')
        ax.spines['left'].set_color('#2E2E2A')
        ax.spines['bottom'].set_color('#2E2E2A')
    
        # Remove tick marks but keep the tick labels
        ax.tick_params(axis='both', which='both', length=0)
    
        # Create scatter plot with grey for non-annotated circles
        scatter = ax.scatter(valid_data[x_metric], valid_data[y_metric], 
                             alpha=0.25, c='#83bd8e', edgecolor='black', s=80, marker='o', label='Players')
    
        # Overlay annotated players in beige
        annotated = ax.scatter(top_players[x_metric], top_players[y_metric], 
                               c='#358244', s=175, marker='o', edgecolor='grey', label='Top Performers', alpha=0.45, zorder=9)
    
        #c='#2e4384', #358281
        # Annotate names of the top players for both metrics, placing above their circles
        for index, row in top_players.iterrows():
            ax.annotate(row['Player Name'], (row[x_metric], row[y_metric]),
                        fontsize=11, color='#d0ceda', alpha=1, ha='center', fontproperties=custom_font, zorder=10)
    
        # Invert y-axis if the selected metric is one of the inverted metrics
        if y_metric in inverted_metrics:
            ax.set_ylim(ax.get_ylim()[::-1])  # Invert y-axis
    
        # Invert x-axis if the selected metric is one of the inverted metrics
        if x_metric in inverted_metrics:
            ax.set_xlim(ax.get_xlim()[::-1])  # Invert x-axis
    
        # Set plot labels and title with custom titles
        plt.title(f'{custom_titles[y_metric]} vs. {custom_titles[x_metric]}', 
                  fontproperties=custom_fontt, ha='left', color='white', y=1.1, x=0, fontsize=28)
        plt.text(0, 1.07, "Per 90 Values | Opta Data as of 09/10 | Code by @DanishScout_", ha='left', fontproperties=custom_font, fontsize=15, color="white", alpha=0.4, transform=plt.gca().transAxes)  # Add the subtitle
        # Set the x and y labels using custom titles and change color to white
        plt.xlabel(custom_titles[x_metric], fontsize=14, fontproperties=custom_font, color='white')
        plt.ylabel(custom_titles[y_metric], fontsize=14, fontproperties=custom_font, color='white')
        
        # Change the ticks color to white
        ax.tick_params(axis='x', colors='white')  # Change x-axis ticks color
        ax.tick_params(axis='y', colors='white')  # Change y-axis ticks color
    
        # Add grid for better readability
        ax.grid(color='gray', linestyle='--', linewidth=0.25)
    
     
        # Define mappings for leagues and positions
        league_mapping = {
            'Superligaen': 'Den1',
            'Allsvenskan': 'Swe1',
            'Eliteserien': 'Nor1',
            'Premier League': 'Eng1',
            'LaLiga': 'Spa1',
            'Bundesliga': 'Ger1',
            'Serie A': 'Ita1',
            'Ligue 1': 'Fra1',
            'Eredivisie': 'Ned1',
            'Liga Portugal': 'Por1',
            'First Division A': 'Bel1',
            'Premiership': 'Sco1',
            'J. League': 'Jap1',
            'Liga Profesional': 'Arg1',
            'Brazilian Serie A': 'Bra1',
            'Austrian Bundesliga': 'Aut1'
        }
    
        # Function to shorten position names
        def shorten_position(position):
            position_mapping = {
                'Right Winger': 'RW',
                'Left Winger': 'LW',
                'Central Midfielder': 'CM',
                'Defensive Midfielder': 'DM',
                'Attacking Midfielder': 'AM',
                'Center Back': 'CB',
                'Right Back': 'RB',
                'Left Back': 'LB',
                'Right Wing-Back': 'RWB',
                'Left Wing-Back': 'LWB',
                'Keeper': 'GK',
                'Striker': 'ST',
                'Left Midfielder': 'LM',
                'Right Midfielder': 'RM'
            }
            return position_mapping.get(position, position)  # Default to original if not found
    
        # Gather the chosen selections
        chosen_leagues = [league_mapping[league] for league in selected_leagues if league in league_mapping]
        chosen_leagues_str = ', '.join(chosen_leagues) if chosen_leagues else 'All leagues'
        
        chosen_positions = [shorten_position(pos) for pos in selected_positions]
        chosen_positions_str = ', '.join(chosen_positions) if chosen_positions else 'All positions'
        
        age_range_str = f'{age_range[0]} - {age_range[1]} years'
        minutes_str = f'Minimum Min. Played: {minutes_range[0]}'
        
        # Create a formatted string for the footer
        chosen_leagues_str = ', '.join([league_mapping[league] for league in selected_leagues]) if selected_leagues else ''
        chosen_positions_str = ', '.join([shorten_position(position) for position in selected_positions]) if selected_positions else ''
        
        # Create the footer text
        footer_text = (f"Chosen Leagues: {chosen_leagues_str}\n"
                       f"Chosen Positions: {chosen_positions_str}\n"
                       f"Selected Team Rank: {selected_team_rank}")
    
        
        # Add footer text to the plot
        plt.text(0, -0.125, footer_text, ha='left', fontproperties=custom_font, fontsize=10, color='white', 
                 alpha=0.6, transform=plt.gca().transAxes, verticalalignment='top')
    
    
        # Create a formatted string for the footer
        footer_text2 = (f"Age Range: {age_range_str}\n"
                         f"{minutes_str}")
    
        
        # Add footer text to the plot
        plt.text(1, -0.125, footer_text2, ha='right', fontproperties=custom_font, fontsize=10, color='white',
                 alpha=0.6, transform=plt.gca().transAxes, verticalalignment='top')
    
        # Button to display the plot
    if st.button("Show Scatter Plot"):
        st.pyplot(plt)

# Finally, call the run function to execute the app
if __name__ == "__main__":
    run()