import requests
import pandas as pd

url = "https://www.sofascore.com/api/v1/team/2817/unique-tournament/7/season/61644/top-players/overall"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Statistiques à extraire
    stats_paths = [
        "goals",
        "expectedGoals",
        "assists",
        "goalsAssistsSum",
        "shotsOnTarget",
        "successfulDribbles",
        "bigChancesCreated"
    ]
    
    players_stats = []

    # Extraction des données
    for stat in stats_paths:
        for player_data in data["topPlayers"].get(stat, []):
            player_name = player_data["player"]["name"]
            stat_value = player_data["statistics"].get(stat, None)
            
            player_entry = next((p for p in players_stats if p["name"] == player_name), None)
            
            if player_entry:
                player_entry[stat] = stat_value
            else:
                player_entry = {"name": player_name, stat: stat_value}
                players_stats.append(player_entry)

    df = pd.DataFrame(players_stats)

    df.to_excel("barcelona_top_players_stats.xlsx", index=False, engine="openpyxl")

    print("- barcelona_top_players_stats.xlsx")

else:
    print("❌ Erreur:", response.status_code)
