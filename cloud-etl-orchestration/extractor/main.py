from api_handlers import fetch_data
from data_processing import data_to_csv
from upload_to_gcs import upload_to_gcs
from config import HEADERS, URL_API_TEAMS, URL_PLAYER_STATISTICS, BUCKET_NAME, QUERY_STRINGS

def download_teams():
    data = fetch_data(URL_API_TEAMS, HEADERS)
    if data and data.get('api', {}).get('teams', []):
        teams = data['api']['teams']
        fields = ['team_id', 'country', 'venue_city', 'name', 'founded', 'venue_name']
        data_to_csv(teams, fields, 'chilean_teams_2024.csv')
        upload_to_gcs('chilean_teams_2024.csv', BUCKET_NAME)

def download_scorers_information():
    json_data = fetch_data(URL_PLAYER_STATISTICS, HEADERS, QUERY_STRINGS)
    if json_data and json_data.get('response', []):
        players_data = json_data['response']
        csv_filename = 'scorers_information_2024.csv'
        
        # Prepare DataFrame
        players = []
        for player_data in players_data:
            player_info = player_data.get('player', {})
            statistics = player_data.get('statistics', [{}])[0]
            team_name = statistics.get('team', {}).get('name', '')
            players.append({
                'firstname': player_info.get('firstname', ''),
                'lastname': player_info.get('lastname', ''),
                'age': player_info.get('age', ''),
                'nationality': player_info.get('nationality', ''),
                'height': player_info.get('height', ''),
                'weight': player_info.get('weight', ''),
                'injured': player_info.get('injured', ''),
                'team': team_name
            })

        # Utilizing data_to_csv for consistent data handling
        fields = ['firstname', 'lastname', 'age', 'nationality', 'height', 'weight', 'injured', 'team']
        data_to_csv(players, fields, 'scorers_information_2024.csv')

        # Upload to GCS
        upload_to_gcs(csv_filename, BUCKET_NAME)
    else:
        print("Failed to fetch data from the API or no data available")


def download_scorers_statistics():
    data = fetch_data(URL_PLAYER_STATISTICS, HEADERS, QUERY_STRINGS)
    if data and data.get('response', []):
        players = data['response']
        fields = [
            'firstname', 'lastname', 'goals', 'assists', 'conceded',
            'penalty_scored', 'penalty_missed', 'total_passes', 'key_passes',
            'total_duels', 'duels_won'
        ]
        rows = [{
            'firstname': p.get('player', {}).get('firstname', ''),
            'lastname': p.get('player', {}).get('lastname', ''),
            'goals': p.get('statistics', [{}])[0].get('goals', {}).get('total', 0),
            'assists': p.get('statistics', [{}])[0].get('goals', {}).get('assists', 0),
            'conceded': p.get('statistics', [{}])[0].get('goals', {}).get('conceded', 0),
            'penalty_scored': p.get('statistics', [{}])[0].get('penalty', {}).get('scored', 0),
            'penalty_missed': p.get('statistics', [{}])[0].get('penalty', {}).get('missed', 0),
            'total_passes': p.get('statistics', [{}])[0].get('passes', {}).get('total', 0),
            'key_passes': p.get('statistics', [{}])[0].get('passes', {}).get('key', 0),
            'total_duels': p.get('statistics', [{}])[0].get('duels', {}).get('total', 0),
            'duels_won': p.get('statistics', [{}])[0].get('duels', {}).get('won', 0)
        } for p in players]

        data_to_csv(rows, fields, 'scorers_statistics_2024.csv')
        upload_to_gcs('scorers_statistics_2024.csv', BUCKET_NAME)

def main():
    download_teams()
    download_scorers_information()
    download_scorers_statistics()

if __name__ == "__main__":
    main()

