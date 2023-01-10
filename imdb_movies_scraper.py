import requests
from bs4 import BeautifulSoup


class Movies:
    def __init__(self, url, pages, rating):
        self.url = url
        self.pages = pages
        self.rating = rating

    def get_movies(self):
        inc = 1
        while inc <= self.pages:
            payload = {'pn': inc}
            try:
                source_code = requests.get(self.url, params=payload)
                soup = BeautifulSoup(source_code.content, 'lxml')
                movie_data = self.get_titles_and_rating(soup)
                # print(movie_data)
                self.choose_movies(movie_data)
                inc += 1
            except requests.exceptions.RequestException as e:
                SystemExit(e)
            except AttributeError as e:
                pass
            except UnicodeError as e:
                pass
            # https: // www.cinemagia.ro / filme - 2022 /? & pn = 2

    @staticmethod
    def get_titles_and_rating(soup):
        titles = [title.text.strip().split('\n')[0] for title in soup.find_all('div', class_='title')]
        titles.pop(-1)
        rating = [r.text.strip() for r in soup.find_all('a', class_='rating-imdb')]
        return dict(zip(titles, rating))

    def choose_movies(self, movie_data):
        for k, v in movie_data.items():
            if float(v[6::]) >= self.rating:
                print(f'{k} -> {v}')


if __name__ == '__main__':
    m = Movies('https://www.cinemagia.ro/filme-2022/', 10, 7.5)
    m.get_movies()
