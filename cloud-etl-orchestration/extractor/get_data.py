import requests
import json
import csv
from config import HEADERS, URL_API_TEAMS, URL_PLAYER_STATISTICS, QUERY_STRINGS

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
                writer.writeheader()
        
                for entry in data:
                    writer.writerow({field: entry.get(field) for field in fields})

            print(f"Data successfully uploaded to {csv_filename}")

        else:
            print(f"No data uploaded to {csv_filename}")
    
    else: print("Failed to fetch data from the API")


def download_scorers_information():
    response = requests.get(URL_PLAYER_STATISTICS, headers=HEADERS, params=QUERY_STRINGS)

    if response.status_code == 200:
        data = response.json().get('response', [])
        csv_filename = 'scorers_information_2024.csv'

        if data:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[
                    'firstname', 'lastname', 'age', 'nationality', 'height', 'weight', 'injured', 'team'
                ])
                writer.writeheader()

                for player_data in data:
                    player_info = player_data.get('player', {})
                    team_name = player_data.get('statistics')[0]['team']['name']

                    writer.writerow({
                        'firstname': player_info.get('firstname', ''),
                        'lastname': player_info.get('lastname', ''),
                        'age': player_info.get('age', ''),
                        'nationality': player_info.get('nationality', ''),
                        'height': player_info.get('height', ''),
                        'weight': player_info.get('weight', ''),
                        'injured': player_info.get('injured', ''),
                        'team': team_name
                    })

                    print(f"Player successfully uploaded to {csv_filename}")
                else:
                    print(f"No player uploaded to {csv_filename}")
        else:
            print("Failed to fetch data from the API")


def download_scorers_statistics():
    
    response = requests.get(URL_PLAYER_STATISTICS, headers=HEADERS, params=QUERY_STRINGS)

    if response.status_code == 200:
        data = response.json().get('response', [])
        csv_filename = 'scorers_statistics_2024.csv'

        if data:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[
                   'firstname', 'lastname', 'goals', 'assists', 'conceded', 'penalty_scored','penalty_missed','total_passes','key_passes','total_duels','duels_won'
                ])
                writer.writeheader()

                for player_data in data:
                    player_info = player_data.get('player', {})
                    statistics = player_data.get('statistics', [{}])


                    
                    goals_data = statistics[0]['goals']
                    penalty_data = statistics[0]['penalty']
                    passes_data = statistics[0]['passes']
                    duels_data = statistics[0]['duels']


                    writer.writerow({
                        'firstname': player_info.get('firstname', ''),
                        'lastname': player_info.get('lastname', ''),
                        'goals': goals_data.get('total', 0),
                        'assists': goals_data.get('assists', 0),
                        'conceded': goals_data.get('conceded', 0),
                        'penalty_scored': penalty_data.get('scored',0),
                        'penalty_missed': penalty_data.get('missed',0),
                        'total_passes': passes_data.get('total',0),
                        'key_passes': passes_data.get('key',0),
                        'total_duels': duels_data.get('total',0),
                        'duels_won': duels_data.get('won',0)
                    })

                    print(f"Player successfully uploaded to {csv_filename}")
                else:
                    print(f"No player uploaded to {csv_filename}")
        else:
            print("Failed to fetch data from the API")

if __name__ == "__main__":
    download_teams()
    download_scorers_information()
    download_scorers_statistics()


