import requests
from bs4 import BeautifulSoup

def get_open_graph_data(url):
    """
    Fetches Open Graph data from a given URL.
    Returns a dictionary with the Open Graph data.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    og_data = {}

    # Extract Open Graph metadata
    og_title = soup.find('meta', property='og:title')
    og_description = soup.find('meta', property='og:description')
    og_url = soup.find('meta', property='og:url')
    og_image = soup.find('meta', property='og:image')
    og_type = soup.find('meta', property='og:type')


    # Add the values to the dictionary
    if og_title:
        og_data['title'] = og_title['content']
    if og_description:
        og_data['description'] = og_description['content']
    if og_url:
        og_data['url_field'] = og_url['content']
    if og_image:
        og_data['url_to_image'] = og_image['content']
    if og_type:
        og_data['type'] = og_type['content']


    return og_data