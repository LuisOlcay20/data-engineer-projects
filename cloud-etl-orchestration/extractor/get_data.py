import requests
import json
import csv
from config import HEADERS, URL_API_TEAMS, URL_PLAYER_STATISTICS, LEAGUE_ID, SEASON

def download_teams():

    response = requests.get(URL_API_TEAMS, headers=HEADERS)

    if response.status_code == 200:
        data = response.json().get('api', {}).get('teams', [])
        csv_filename = 'chilean_teams_2024.csv'

        if data:
            fields = ['team_id','country','venue_city','name','founded','venue_name']

            # Write data into CSV     
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
        
                for entry in data:
                    writer.writerow({field: entry.get(field) for field in fields})

            print(f"Data successfully uploaded to {csv_filename}")

        else:
            print(f"No data uploaded to {csv_filename}")
    
    else: print("Failed to fetch data from the API")

def download_top_scorers():
    query_strings = {"league": LEAGUE_ID, "season": SEASON}
    response = requests.get(URL_PLAYER_STATISTICS, headers=HEADERS, params=query_strings)

    if response.status_code == 200:
        data = response.json().get('response', [])
        csv_filename = 'top_scorers_2024.csv'

        if data:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[
                    'firstname', 'lastname', 'age', 'team_name', 'total_goals', 'assists', 'saves', 'conceded'
                ])
                writer.writeheader()

                for player_data in data:
                    player_info = player_data.get('player', {})
                    statistics = player_data.get('statistics', [{}])

                    # Team name
                    team_name = statistics[0]['team']['name']

                    # Goals data
                    goals_data = statistics[0]['goals']

                    writer.writerow({
                        'firstname': player_info.get('firstname', ''),
                        'lastname': player_info.get('lastname', ''),
                        'age': player_info.get('age', ''),
                        'team_name': team_name, 
                        'total_goals': goals_data.get('total', 0),
                        'assists': goals_data.get('assists', 0),
                        'saves': goals_data.get('saves', 0),  
                        'conceded': goals_data.get('conceded', 0)
                    })

                    print(f"Data successfully uploaded to {csv_filename}")
                else:
                    print(f"No data uploaded to {csv_filename}")
        else:
            print("Failed to fetch data from the API")

if __name__ == "__main__":
    download_top_scorers()
