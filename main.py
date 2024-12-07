from flask import Flask, render_template, request, jsonify
import pandas as pd
from injury_finder import player_injury_record
from information_finder_functions import get_season_stats_player, get_manager_history
from match_probability import calculate_team_score, return_probabilities

app = Flask(__name__)

players_df = pd.read_csv('Football-Data/Players_List.csv')
team_df = pd.read_csv('Football-Data/Team_List.csv')
manager_df = pd.read_csv('Football-Data/Manager_List.csv')
player_ratings = {}

@app.route('/')
def home_screen():
    '''
    Renders the home page of the API from header.html

    Input: Nothing

    Output: HTML Page header.html rendered.
    '''
    return render_template('header.html')

@app.route('/managerpage', methods=['GET', 'POST'])
def manager_search():
    '''
    Route meant for gathering and uploading data for managers from the Dataframes.

    It listens to 'GET' and 'POST' requests to /managerpage, The function searches for the provided name in
    manager_df. If a name is found, the information is gathered, converted to a record-oriented dictionary, and the
    html template for the managerpage.html is rendered with the data manager_data. Data on the Team Logo is gathered
    from the team_df. The manager data history is scraped dynamically using the get_manager_history function

    Inputs: None

    Outputs: Returns the managerpage.html template with the appropriate response handled based on the name entered.
    and the data provided.
    '''
    if request.method == 'POST':
        manager_name = request.form['name']
        if manager_name:
            manager_row = manager_df[manager_df['Names'].str.lower() == manager_name.lower()]
            if not manager_row.empty:
                manager_data = manager_row.to_dict(orient='records')[0]
                manager_data['Team Logo Link'] = team_df[team_df['Squad'].str.lower() == manager_data['Team'].lower()].iloc[0]['Team Logo Link']
                manager_data['History'] = get_manager_history(manager_data['Page Link'])
                return render_template('managerpage.html', manager_data=manager_data)
            else:
                return render_template('managerpage.html', error=f"No player found for {manager_name}")
    return render_template('managerpage.html')

@app.route('/playerpage', methods=['GET', 'POST'])
def player_search():
    '''
    Route meant for gathering and uploading data for players from the Dataframes.

    It listens to 'GET' and 'POST' requests to /playerpage, The function searches for the provided name in
    player_df. If a name is found, the information is gathered, converted to a record-oriented dictionary, and the
    html template for the playerpage.html is rendered with the data player_data. Data on the Team Logo
    and League Logo is gathered from the team_df. The player's current stats is scraped dynamically using the
    get_season_stats_player function, and the player ratings functionality is handled as well.

    Inputs: None

    Outputs: Returns the playerpage.html template with the appropriate response handled based on the name entered.
    and the data provided.
    '''
    if request.method == 'POST':
        player_name = request.form['name']
    elif request.method == 'GET':
        player_name = request.args.get('player_name')
    else:
        player_name = None
    if player_name:
        player_row = players_df[players_df['Names'].str.lower() == player_name.lower()]
        if not player_row.empty:
            player_data = player_row.to_dict(orient='records')[0]
            team_row = team_df[team_df['Squad'].str.lower() == player_data['Team'].lower()]
            team_logo_link = team_row.iloc[0]['Team Logo Link']
            league_logo_link = team_row.iloc[0]['League Logo Link']
            player_data["TeamLogo"] = team_logo_link
            player_data["LeagueLogo"] = league_logo_link
            player_injury_history = player_injury_record(player_data['Name ID'], player_data['ID'])
            player_data["Injury History"] = player_injury_history
            player_data["Current Stats"] = get_season_stats_player(player_data['Name ID'], player_data['ID'], player_data['Roles'])
            player_id = player_data.get('ID')
            current_rating = player_ratings.get(player_id, 0)
            player_data['Current Rating'] = current_rating
            return render_template('playerpage.html', player_data=player_data)
        else:
            return render_template('playerpage.html', player_data=None, error=f"No player found for {player_name}")
    return render_template('playerpage.html', player_data=None)

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    '''
    Handles the submission of player ratings via a POST request. The function stores the submitted rating in the
    a dictionary and returns a response confirming storage.

    Inputs: None

    Output: A JSON response with success of rating submission and the associated rating.
    '''
    data = request.get_json()
    player_id = data['player_id']
    rating = int(data['rating'])
    player_ratings[player_id] = rating
    return jsonify({"success": True, "rating": rating})

@app.route('/teampage', methods=['GET', 'POST'])
def team_search():
    '''
    Route meant for gathering and uploading data for teams from the Dataframes.

    It listens to 'GET' and 'POST' requests to /teampage, The function searches for the provided name in
    team_df. If a name is found, the information is gathered, converted to a record-oriented dictionary, and the
    html template for the teampage.html is rendered with the data team_data. Data on the Player List is gathered
    from the players_df DataFrame, giving a list of all of the players that play for the queried team. On the side
    the functions calculate_team_score and return_probabilities give the three probabilities for win, draw, lose
    for the page.

    Inputs: None

    Outputs: Returns the teampage.html template with the appropriate response handled based on the name entered.
    and the data provided.
    '''
    if request.method == 'POST':
        team_name = request.form['name']
    elif request.method == 'GET':
        team_name = request.args.get('team_name')
    else:
        team_name = None
    if team_name:
        team_row = team_df[team_df['Squad'].str.lower() == team_name.lower()]
        if not team_row.empty:
            player_list = players_df[players_df['Team'].str.lower() == team_name.lower()]
            opp_row = team_df[team_df['Squad'].str.lower() == team_row['Opponent'].iloc()[0].lower()]
            main_keys = ['Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'Last 5']
            team_data = team_row.to_dict(orient="records")[0]
            main_data = {k: team_row.iloc[0][k] for k in main_keys if k in team_row.columns}
            opp_data = {k: opp_row.iloc[0][k] for k in main_keys if k in opp_row.columns}
            main_strength = calculate_team_score(main_data)
            opp_strength = calculate_team_score(opp_data)
            team_a_win, team_b_win, draw = return_probabilities(main_strength, opp_strength)
            team_data['Team Win'] = team_a_win
            team_data['Team Loss'] = team_b_win
            team_data['Draw'] = draw
            team_data['Last 5'] = '/'.join(team_data['Last 5'].split())
            team_data['Player List'] = player_list['Names'].to_list()
            team_data['Opponent Logo Link'] = opp_row.iloc()[0]['Team Logo Link']
            return render_template('teampage.html', team_data=team_data)
        else:
            return render_template('teampage.html', error=f"No team found for {team_name}")
    return render_template('teampage.html')

@app.route('/teampage')
def transition_team():
    '''
    Renders the base team-page template

    Inputs: None

    Output: teampage.html opening page rendered
    '''
    return render_template('teampage.html')

@app.route('/playerpage')
def transition_player():
    '''
    Renders the base player-page template

    Inputs: None

    Output: playerpage.html opening page rendered
    '''
    return render_template('playerpage.html')

@app.route('/managerpage')
def transition_manager():
    '''
    Renders the base manager-page template

    Inputs: None

    Output: managerpage.html opening page rendered
    '''
    return render_template('managerpage.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
