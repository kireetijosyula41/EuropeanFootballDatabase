from flask import Flask, render_template, request
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

players_df = pd.read_csv('Football-Data/Players.csv')

@app.route('/')
def home_screen():
    return render_template('header.html')

@app.route('/playerpage')
def transition_player():
    return render_template('playerpage.html')

@app.route('/managerpage')
def transition_manager():
    return render_template('managerpage.html')

@app.route('/teampage')
def transition_team():
    return render_template('teampage.html')

def get_player_stats(player_url):
    start_time = time.time()
    response = requests.get(player_url)
    elapsed_time = time.time() - start_time
    print(f"Time taken for {player_url}: {elapsed_time} seconds")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find('img', class_='data-header__profile-image')
        image_url = image_tag['src'] if image_tag else None
        return {'image_url': image_url}
    else:
        return {'image_url': None}

@app.route('/playerpage', methods=['GET', 'POST'])
def player_search():
    if request.method == 'POST':
        player_name = request.form['name']
        if player_name:
            player_row = players_df[players_df['Names'].str.lower() == player_name.lower()]
            if not player_row.empty:
                player_data = player_row.to_dict(orient='records')[0]
                player_url = player_data.get('Player Profile Link')
                stats = get_player_stats(player_url)
                player_data.update(stats)
                return render_template('playerpage.html', player_data=player_data)
            else:
                return render_template('playerpage.html', error=f"No player found for {player_name}")
    return render_template('playerpage.html')

if __name__ == '__main__':
    app.run(debug=True)