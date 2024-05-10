import requests

def fetch_data(url, headers, params=None):
    """
    Fetches data from the specified API endpoint. 
    Returns:
        dict: JSON response data.
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
