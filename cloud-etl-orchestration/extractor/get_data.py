import requests
import json
import csv
from config import URL_API_TEAMS, RAPIDAPI_KEY, RAPIDAPI_HOST

def download_teams():

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(URL_API_TEAMS, headers=headers)

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

if __name__ == "__main__":
    download_teams()

