import sys
import sqlite3
from omdb import get_movie_data


class Movie(object):
    def __init__(self):
        self.sql_connection = sqlite3.connect('Backend_movies.sqlite')
        self.c = self.sql_connection.cursor()

        self.title = None
        self.year = None
        self.runtime = None
        self.genre = None
        self.director = None
        self.cast = None
        self.writer = None
        self.language = None
        self.country = None
        self.awards = None
        self.imdb_rating = None
        self.imdb_votes = None
        self.box_office = None

    def _close_connection(self):
        self.sql_connection.close()

    def get_movie_from_db(self, movie_title):
        movie_data = self.c.execute('SELECT * FROM movies WHERE title = ?', (movie_title,)).fetchone()
        self.title = movie_data[1]
        self.year = movie_data[2]
        self.runtime = movie_data[3]
        self.genre = movie_data[4]
        self.director = movie_data[5]
        self.cast = movie_data[6]
        self.writer = movie_data[7]
        self.language = movie_data[8]
        self.country = movie_data[9]
        self.awards = movie_data[10]
        self.imdb_rating = movie_data[11]
        self.imdb_votes = movie_data[12]
        self.box_office = movie_data[13]

        self._close_connection()

    def save(self):
        try:
            self.c.execute('UPDATE movies SET '
                           'YEAR=?, RUNTIME=?, GENRE=?, DIRECTOR=?, "CAST"=?, WRITER=?, LANGUAGE=?,'
                           ' COUNTRY=?, AWARDS=?, IMDb_Rating=?, IMDb_votes=?, BOX_OFFICE=?'
                           ' WHERE TITLE=?',
                           [self.year,
                            self.runtime,
                            self.genre,
                            self.director,
                            self.cast,
                            self.writer,
                            self.language,
                            self.country,
                            self.awards,
                            self.imdb_rating,
                            self.imdb_votes,
                            self.box_office,
                            self.title]
                           )
            self.sql_connection.commit()
            print(f'Updated done for {self.title}')
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
        finally:
            self.sql_connection.set_trace_callback(print)
            self.sql_connection.close()

    def __str__(self):
        return f'{self.title}, {self.year}'


def update_movie(movie_title):
    movie_data = get_movie_data(movie_title)
    movie = Movie()

    movie.title = movie_data['Title']
    movie.year = movie_data['Year']
    movie.runtime = movie_data['Runtime']
    movie.genre = movie_data['Genre']
    movie.director = movie_data['Director']
    movie.cast = movie_data['Actors']
    movie.writer = movie_data['Writer']
    movie.language = movie_data['Language']
    movie.country = movie_data['Country']
    movie.awards = movie_data['Awards']
    movie.imdb_rating = movie_data['imdbRating']
    movie.imdb_votes = movie_data['imdbVotes']
    movie.box_office = movie_data['BoxOffice']

    movie.save()
