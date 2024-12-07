import requests
from bs4 import BeautifulSoup

def player_injury_record(player_name, player_id):
    '''
    Purpose: Scrape page in order to find player's recent injury history

    Input: player_name: Transfermarkt's unique name-id string given to each player
    Input: player_id:

    Output: Returns a list of FOUR OR LESS 3-Tuples, storing the injury type, start date and end date.
    '''
    injury_history_list = []
    page = f"https://www.transfermarkt.us/{player_name}/verletzungen/spieler/{player_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    pageTree = requests.get(page, headers = headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    injury_history = pageSoup.find("div", {"class": "responsive-table"}).find_all("td", {"class": ["hauptlink", "zentriert", "rehtcs"]})
    for i in range(0, len(injury_history), 5):
        soup1 = BeautifulSoup(str(injury_history[i+1]), 'html.parser').text.strip()
        soup2 = BeautifulSoup(str(injury_history[i+2]), 'html.parser').text.strip()
        soup3 = BeautifulSoup(str(injury_history[i+3]), 'html.parser').text.strip()
        if soup3 == '':
            soup3 = 'unknown'
        injury_history_list.append((soup1, soup2, soup3))
    if len(injury_history_list) >= 4:
        return injury_history_list[0:4]
    return injury_history_list