import requests
from bs4 import BeautifulSoup

def get_season_stats_player(name_id, player_id, role):
    '''
    Dynamically fetches performance data for a player for the current season (in all competitions)

    Input: name_id = name-string unique for a player, assigned by Transfermarkt
    Input: player_id = number string unique for a player, assigned by Transfermarkt
    Input: role = one of 'Goalkeeper', 'Defender', 'Midfielder', or 'Attacker'.

    Output: List of three values detailing a player's appearances, goals, and assists
    for the season (for defenders, midfielders, attackers), or a player's appearances, goals conceded
    and clean sheets (for goalkeepers).
    '''
    page = f"https://www.transfermarkt.us/{name_id}/leistungsdaten/spieler/{player_id}/plus/0?saison=2024"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    pageTree = requests.get(page, headers = headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    season_stats = pageSoup.find("div", {"class": "responsive-table"}).find_all("td", {"class": "zentriert"})
    stats_list_final = ['0', '0', '0']
    if season_stats:
        if role == 'Goalkeeper':
            appearances = BeautifulSoup(str(season_stats[0]), 'html.parser').text.strip()
            goals = BeautifulSoup(str(season_stats[5]), 'html.parser').text.strip()
            assists = BeautifulSoup(str(season_stats[6]), 'html.parser').text.strip()
        else:
            appearances = BeautifulSoup(str(season_stats[0]), 'html.parser').text.strip()
            goals = BeautifulSoup(str(season_stats[1]), 'html.parser').text.strip()
            assists = BeautifulSoup(str(season_stats[2]), 'html.parser').text.strip()
        stats_list = [appearances, goals, assists]
        stats_list_final = ['0' if i == '-' else i for i in stats_list]
    return stats_list_final

def get_manager_history(manager_url):
    '''
    Dynamically fetches a manager's employment history from Transfermarkt.

    Input: manager_url: Manager's home page on Transfermarkt

    Output: List of 3-tuples, where each tuple has the team the manager managed, when the started
    management, and when they ended management for that team.
    '''
    print(manager_url)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    pageTree = requests.get(manager_url, headers = headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    History_Table = pageSoup.find("div", {"class": "responsive-table"}).find_all("td", {"class": ["zentriert",
                                                                                                  "hauptlink no-border-links"]})
    final_info = []
    for i in range(0, len(History_Table), 5):
        soup = BeautifulSoup(str(History_Table[i]), 'html.parser')
        titles = [tag['title'] for tag in soup.find_all(title=True) if tag['title'] != '\xa0']
        unique_titles = list(set(titles))[0]
        start = BeautifulSoup(str(History_Table[i + 2]), 'html.parser').text.strip()
        end = ": ".join(BeautifulSoup(str(History_Table[i + 3]), 'html.parser').text.strip().split('\xa0'))
        final_info.append((unique_titles, start, end))
    return final_info