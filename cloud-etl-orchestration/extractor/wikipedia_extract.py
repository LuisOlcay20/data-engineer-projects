import requests
from bs4 import BeautifulSoup


def get_wikipedia_data(url):
    """
    Retrieves the HTML content of a Wikipedia page from the given URL
    """
    try:
        response = requests.get(url, timeout=10)  
        response.raise_for_status()  # Check if the request is successful
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def clean_text(text):
    """
    Clean the text data by removing unnecessary characters
    """
    text = str(text).strip()
    text = text.replace('&nbsp', '')
    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]

    return text.replace('\n', '')

def extract_stadium_data(html):
    """
    Extracts stadium data from HTML content
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all("table", {"class": "wikitable sortable"})[0]

    table_rows = table.find_all('tr')

    data = []

    for i in range(1, len(table_rows)):
        tds = table_rows[i].find_all('td')
        values = {
            'stadium': clean_text(tds[0].text),
            'capacity': clean_text(tds[1].text).replace(',', '').replace('.', ''),
            'country': clean_text(tds[2].text),
            'city': clean_text(tds[3].text),
            'teams': clean_text(tds[4].text),
        }
        data.append(values)

    return data



