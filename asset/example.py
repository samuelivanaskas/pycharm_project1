import time
import random
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = BeautifulSoup(requests.get(movie_link, headers=headers).content, 'html.parser')
    movie_soup = response

    if movie_soup is not None:
        title = None
        date = None
        plot_text = None

        movie_data = movie_soup.find('div', attrs={'class': 'sc-385ac629-3 kRUqXl'})
        if movie_data is not None:
            title = movie_data.find('h1').get_text()
            date = movie_data.find('a', attrs={'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).get_text().strip()

        plot_text_element = movie_soup.find('span', attrs={'class': 'sc-6a7933c5-1 fPmRoa'})
        if plot_text_element is not None:
            plot_text = plot_text_element.get_text().strip()

        return title, date, plot_text

def scrape_imdb_top_250():
    url = 'https://www.imdb.com/chart/top/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_links = []

    for movie in soup.select('td.titleColumn a'):
        movie_link = 'https://www.imdb.com' + movie.get('href')
        movie_links.append(movie_link)

    movie_details_list = []
    for link in movie_links:
        movie_details = extract_movie_details(link)
        movie_details_list.append(movie_details)

    return movie_details_list

if __name__ == "__main__":
    top_250_movies_details = scrape_imdb_top_250()
    for idx, details in enumerate(top_250_movies_details, start=1):
        title, date, plot_text = details
        print(f"{idx}. Title: {title}\n   Date: {date}\n   Plot: {plot_text}\n")
