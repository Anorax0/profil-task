import sqlite3
from omdb import get_movie_data


class Movies(object):
    def __init__(self):
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

    def _open(self):
        self.sql_connection = sqlite3.connect('Backend_movies.sqlite')
        self.c = self.sql_connection.cursor()

    def _close(self):
        self.sql_connection.close()

    def get_movies_list(self):
        """
        Returns list of movies' titles from database
        :return: list
        """
        self._open()
        movies_list = self.c.execute('SELECT title FROM movies').fetchall()
        self._close()
        return movies_list

    def __str__(self):
        return f'{self.title}, {self.year}'


class MoviesSorted(Movies):
    def __init__(self):
        super(MoviesSorted, self).__init__()

    def sort_by(self, selection=('title', ), order_by=('year', ), order_way="DESC", query_limit=10):

        self._open()
        output = None
        selection_format = ', '.join((str(x) for x in selection))
        order_by_format = ', '.join(str(x) for x in order_by)

        if 'cast' in selection_format and 'cast' in order_by_format:
            selection_format = selection_format.replace("cast", "\"CAST\"")
            order_by_format = order_by_format.replace("cast", "\"CAST\"")

        try:
            query = "SELECT {} FROM movies ORDER BY {} {} LIMIT {}".format(selection_format,
                                                                           order_by_format,
                                                                           order_way,
                                                                           query_limit)
            output = self.c.execute(query).fetchall()

        except sqlite3.OperationalError as e:
            output = 'You are trying to access not existing value: ', e
        finally:
            self._close()
            return output

    def highscored(self):
        highscored = []
        highscored.append(self.sort_by(selection=['title', 'runtime'], order_by=['Runtime'], query_limit=1))
        highscored.append(self.sort_by(selection=['title', 'box_office'], order_by=['Box_Office'], query_limit=1))
        # highscored.append(self.sort_by(order_by=['awards'], query_limit=1))
        # highscored.append(self.sort_by(order_by=['nominations'], query_limit=1))
        # highscored.append(self.sort_by(order_by=['oscars'], query_limit=1))
        # highscored.append(self.sort_by(order_by=['imdb_dating'], query_limit=1))
        return highscored


class MovieDB(Movies):
    def __init__(self):
        super(MovieDB, self).__init__()

    def clean(self):
        """
        Updates movies' titles with no extra space titles
        :return: None
        """
        # db needs to be cleaned due to extra space in title "The Green Mile "
        movie_list = self.get_movies_list()
        for name in movie_list:
            if len(name[0]) != len(name[0].strip()):
                self.title = name[0].strip()
                self._open()
                self.c.execute('UPDATE movies SET title = ? WHERE title = ?', (self.title, name[0]))
                self.sql_connection.commit()
                self._close()
        return None

    def get_movie_from_db(self, movie_title=None):
        """
        Updates instance's variable with data from database
        :param movie_title:
        :return:
        """
        if movie_title is None:
            movie_title = self.title
        self._open()

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

        self._close()

        return 'ACCESS DENIED: Please use instance\'s reference variable to obtain certain value'

    def save(self):
        """
        Updates database with instance's values
        :return: str
        """

        self._open()

        try:
            self.c.execute('UPDATE movies SET '
                           'YEAR=?, RUNTIME=?, GENRE=?, DIRECTOR=?, "CAST"=?, WRITER=?, LANGUAGE=?,'
                           ' COUNTRY=?, AWARDS=?, IMDb_Rating=?, IMDb_votes=?, BOX_OFFICE=?'
                           ' WHERE TITLE=?',
                           (self.year,
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
                            self.title)
                           )
            self.sql_connection.commit()
            return f'Update done for "{self.title}" movie.'

        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]
        finally:
            self.sql_connection.close()

    def update_movie(self, movie_title):
        """
        Updates instance's variables by omdb api
        :param movie_title: str
        :return: func save
        """

        movie_data = get_movie_data(movie_title)

        self.title = movie_data.get('Title', None)
        self.year = movie_data.get('Year', None)
        if movie_data.get('Runtime', None).split()[0].isdigit():
            self.runtime = int(movie_data.get('Runtime', None).split()[0])
        else:
            self.runtime = 'N/A'
        self.genre = movie_data.get('Genre', None)
        self.director = movie_data.get('Director', None)
        self.cast = movie_data.get('Actors', None)
        self.writer = movie_data.get('Writer', None)
        self.language = movie_data.get('Language', None)
        self.country = movie_data.get('Country', None)
        self.awards = movie_data.get('Awards', None)
        self.imdb_rating = float(movie_data.get('imdbRating', None))
        self.imdb_votes = int((movie_data.get('imdbVotes', None)).replace(",", ""))
        if movie_data.get('BoxOffice', None) != 'N/A' and movie_data.get('BoxOffice', None) is not None:
            self.box_office = int(movie_data.get('BoxOffice', None)[1:].replace(",", ""))

        return self.save()


if __name__ == '__main__':
    # module's tests
    # from pprint import pprint
    movie = MovieDB()
    movie.update_movie('Coco')
    print(movie.imdb_votes)
    print(type(movie.imdb_votes))