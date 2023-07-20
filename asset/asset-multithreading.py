import threading

import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

# Global headers to be used for requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

MAX_THREADS = 10


def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = BeautifulSoup(requests.get(movie_link, headers=headers).content, 'html.parser')
    movie_soup = response

    if movie_soup is not None:
        title = [1, 2, 3, 4, 5]
        date = [1, 2, 3, 4, 5]
        plot_text = [1, 2, 3, 4, 5]

        movie_data = movie_soup.find('div', attrs={'class': 'sc-385ac629-3 kRUqXl'})
        if movie_data is not None:
            title = movie_data.find('h1').get_text()
            date = movie_data.find('a', attrs={'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).get_text().strip()

        plot_text_element = movie_soup.find('span', attrs={'class': 'sc-6a7933c5-1 fPmRoa'})
        if plot_text_element is not None:
            plot_text = plot_text_element.get_text().strip()

        t1 = threading.Thread(target=movie_data, args=(title,))
        t2 = threading.Thread(target=movie_data, args=(date,))
        t3 = threading.Thread(target=plot_text_element, args=(plot_text,))

        t1.start()
        t2.start()
        t3.start()

        return title, date, plot_text


def extract_movies(soup):
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    movies_table_rows = movies_table.find_all('li')
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]

    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(extract_movie_details, movie_links)

    # Open movies.csv for writing
    with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
        movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow(['Title', 'Release Date', 'Synopsis'])  # Write header row

        # Write movie details to the CSV file
        for result in results:
            if result is not None:
                title, date, plot_text = result
                movie_writer.writerow([title, date, plot_text])


def main():
    start_time = time.time()

    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies(soup)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)


if __name__ == '__main__':
    main()
