import sqlite3
from omdb import get_movie_data


class Movies(object):
    def __init__(self):
        """
        Initialize basic movie instance - it needs to be reinitialized
        or delete/create every time new instance is created
        """
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
        """
        Opens connection with database
        :return: None
        """
        self.sql_connection = sqlite3.connect('Backend_movies.sqlite')
        self.c = self.sql_connection.cursor()
        return None

    def _close(self):
        """
        Closes connection with database
        :return: None
        """
        self.sql_connection.close()
        return None

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
        """
        Initialize class instance as child of Movies class
        """
        super(MoviesSorted, self).__init__()

    def sort_by(self, selection=('title',), where_clause=None, order_by=('year',), order_way="DESC", query_limit=10,
                value=None):

        # opens db connection
        self._open()
        output = None
        selection_format = ', '.join((str(x) for x in selection))
        order_by_format = ', '.join(str(x) for x in order_by)

        if 'cast' in selection_format and 'cast' in order_by_format:
            selection_format = selection_format.replace("cast", "\"CAST\"")
            order_by_format = order_by_format.replace("cast", "\"CAST\"")

        if 'runtime' in selection_format and 'runtime' in order_by_format:
            order_by_format = order_by_format.replace("runtime", "CAST(runtime AS INT)")

        if value in ['int']:
            max_limit = len(self.c.execute("SELECT id FROM movies").fetchall())
            query_limit = max_limit

        try:
            query = f"SELECT {selection_format} FROM movies {where_clause}" \
                    f" ORDER BY {order_by_format} {order_way} LIMIT {query_limit}"
            output = self.c.execute(query).fetchall()

        except sqlite3.OperationalError as e:
            output = ['You are trying to access not existing value: ', e]
        finally:
            self._close()
            if 'awards' in selection:
                output.append(('Little tip:', 'To see awards details use --highscores or -hs.'))
            return output

    @staticmethod
    def extract_tops(query):
        top_oscars = ['title', 0]
        top_nominations = ['title', 0]
        top_other_wins = ['title', 0]
        for x in query:
            search = x[1].split()
            if 'Oscars.' in search and isinstance((search.index('Oscars.') - 1), int) \
                    and search[search.index('Oscars.') - 2] == 'Won':
                if int(search[1]) > top_oscars[1]:
                    top_oscars = [x[0], int(search[1])]

            if 'nominations.' in search and isinstance((search.index('nominations.') - 1), int):
                if int(search[search.index('nominations.') - 1]) > top_nominations[1]:
                    top_nominations = [x[0], int(search[search.index('nominations.') - 1])]

            if 'wins' in search and isinstance((search.index('wins') - 1), int):
                if int(search[search.index('wins') - 1]) > top_other_wins[1]:
                    top_other_wins = [x[0], int(search[search.index('wins') - 1])]

        return top_oscars, top_nominations, top_other_wins

    def get_top_runtime(self):
        """
        Returns list of (title:str, rating:str) of highest runtime
        :return: list
        """

        self._open()
        top_runtime = self.c.execute("SELECT title, runtime FROM movies ORDER BY CAST(runtime AS INT) DESC").fetchone()
        self._close()
        return top_runtime

    def highscored(self):
        highscored = {
            # I wanted to write runtime using sort_by method, but after a long time coding that, I use this, easier.
            'Runtime': self.get_top_runtime(),
            'Box Office': self.sort_by(selection=['title', 'box_office'],
                                       order_by=['Box_Office'],
                                       query_limit=1),
            'Nominations': self.extract_tops(self.sort_by(selection=['title', 'awards'],
                                                          where_clause='WHERE awards LIKE \'Won%Oscars%\'',
                                                          order_by=['AWARDS'],
                                                          query_limit=100)),
            'Imdb Rating': self.sort_by(selection=['title', 'IMDb_Rating'],
                                        order_by=['imdb_rating'],
                                        query_limit=1)}
        return highscored

    def filter_by(self, selection=('title',), filtering_criterion=(), filtering_value=None, query_limit=10):
        self._open()
        selection_format = ', '.join((str(x) for x in selection))
        selection_format = selection_format.replace("cast", "\"CAST\"")
        filtering_criterion = filtering_criterion.replace("cast", "\"CAST\"")
        try:
            if filtering_value.isdigit():
                query = f"SELECT {selection_format} FROM movies " \
                        f"WHERE CAST({filtering_criterion} AS INT) > {filtering_value} LIMIT {query_limit}"
            else:
                query = f"SELECT {selection_format} FROM movies " \
                        f"WHERE {filtering_criterion} LIKE '%{filtering_value}%' LIMIT {query_limit}"
            output = self.c.execute(query).fetchall()
        except sqlite3.OperationalError:
            raise Exception('\n\nCannot procced query. Please check spelling or use << --help >> command.')
        self._close()
        return output

    def compare(self, comparing_criterion, comparing_values):
        self._open()
        output = None
        comparing_criterion = comparing_criterion.replace("cast", "\"CAST\"")

        if comparing_criterion in ('oscars', 'nominations', 'wins', 'awards'):
            oscars_first, nominations_first, wins_first = self.extract_tops(
                self.sort_by(selection=['title', 'awards'],
                             where_clause=f'WHERE title="{comparing_values[0]}"',
                             order_by=['AWARDS'],
                             query_limit=1))
            oscars_second, nominations_second, wins_second = self.extract_tops(
                self.sort_by(selection=['title', 'awards'],
                             where_clause=f'WHERE title="{comparing_values[1]}"',
                             order_by=['AWARDS'],
                             query_limit=100))

            if int(oscars_first[1]) > int(oscars_second[1]):
                output = f'Won Oscars of {oscars_first[0]} is greater' \
                         f' than Oscars of {oscars_second[0]} [{oscars_first[1]} > {oscars_second[1]}]'
            elif int(oscars_first[1]) < int(oscars_second[1]):
                output = f'Won Oscars of {oscars_first[0]} is smaller' \
                         f' than Oscars of {oscars_second[0]} [{oscars_first[1]} > {oscars_second[1]}]'
            elif int(oscars_first[1]) == int(oscars_second[1]):
                output = f'Won Oscars of {oscars_first[0]} is equal' \
                         f' to Oscars of {oscars_second[0]} [{oscars_first[1]} > {oscars_second[1]}]'

            if int(nominations_first[1]) > int(nominations_second[1]):
                output += f'\nAmount of nominations of {nominations_first[0]} is greater than nominations of ' \
                          f'{nominations_second[0]} [{nominations_first[1]} > {nominations_second[1]}]'
            elif int(nominations_first[1]) < int(nominations_second[1]):
                output += f'\nAmount of nominations of {nominations_first[0]} is smaller than nominations of ' \
                          f'{nominations_second[0]} [{nominations_first[1]} > {nominations_second[1]}]'
            elif int(nominations_first[1]) == int(nominations_second[1]):
                output += f'\nAmount of nominations of {nominations_first[0]} is equal to nominations of ' \
                          f'{nominations_second[0]} [{nominations_first[1]} > {nominations_second[1]}]'

            if int(wins_first[1]) > int(wins_second[1]):
                output += f'\nOther wins of {wins_first[0]} is greater' \
                          f' than other wins of {wins_second[0]} [{wins_first[1]} > {wins_second[1]}]'
            elif int(wins_first[1]) < int(wins_second[1]):
                output += f'\nOther wins of {wins_first[0]} is smaller' \
                          f' than other wins of {wins_second[0]} [{wins_first[1]} > {wins_second[1]}]'
            elif int(wins_first[1]) == int(wins_second[1]):
                output += f'\nOther wins of {wins_first[0]} is equal' \
                          f' to other wins of {wins_second[0]} [{wins_first[1]} > {wins_second[1]}]'

        elif comparing_criterion in ('year', 'runtime', 'imdb_rating', 'imdb_votes', 'box_office'):

            query_first = f'SELECT title, {comparing_criterion} FROM movies WHERE title="{comparing_values[0]}"'
            query_second = f'SELECT title, {comparing_criterion} FROM movies WHERE title="{comparing_values[1]}"'
            output_first = self.c.execute(query_first).fetchone()
            output_second = self.c.execute(query_second).fetchone()

            if None in output_first or None in output_second:
                output = 'Cannot compare value that do not exists.'
            elif float(output_first[1]) > float(output_second[1]):
                output = f'{comparing_criterion.title()} of {output_first[0]} is greater than ' \
                         f'{comparing_criterion.title()} of {output_second[0]} [{output_first[1]} > {output_second[1]}]'
            elif float(output_first[1]) == float(output_second[1]):
                output = f'{comparing_criterion.title()} of {output_first[0]} is equal' \
                         f' to {comparing_criterion} of {output_second[0]} [{output_first[1]} = {output_second[1]}]'
            else:
                output = f'{comparing_criterion.title()} of {output_first[0]} is smaller' \
                         f' than {comparing_criterion} of {output_second[0]} [{output_first[1]} < {output_second[1]}]'

            if output is None:
                output = 'Nothing to show. Check spelling or accept the lack of data.'

        self._close()
        return output


class MovieDB(Movies):
    def __init__(self):
        """
        Initialize class instance as child of Movies class
        """
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
        Updates instance's variable with data from database - needs to be reinit, delete/create with every new instance
        :param movie_title: str
        :return: None
        """
        if movie_title is None:
            movie_title = self.title
        self._open()

        movie_data = self.c.execute('SELECT * FROM movies WHERE title = ?', (movie_title,)).fetchone()

        if movie_data is None:
            return 'Cannot find the movie. Consider adding this movie by << add \'title\' >> function.'
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
            self._close()

    def update_movie(self, movie_title):
        """
        Updates instance's variables by omdb api
        :param movie_title: str
        :return: func save
        """

        movie_data = get_movie_data(movie_title)
        if False in movie_data:
            return False

        try:
            # if not movie_data[0]:
            #     raise Exception(f'Cannot retrieve data for {movie_title}. Please check spelling.')

            self.title = movie_data.get('Title', None)
            if self.title[-1] == ' ':
                return f'Cannot update {self.title} due to extra space in title. Please use << clean >> function.'
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
        except KeyError:
            raise Exception('Cannot update - probably database needs to be cleaned - use << clean >> command.')

    def add_movie(self, movie_title):
        self._open()
        self.c.execute(f'INSERT INTO movies (title) VALUES ("{movie_title}")')
        self.sql_connection.commit()
        adding_movie = self.update_movie(movie_title)

        if adding_movie is False:
            print(f'Cannot find movie {movie_title}. Please check spelling.')

        self._close()
        return f'{movie_title} added and updated in database.'


if __name__ == '__main__':
    # module's tests
    # movie = MoviesSorted()
    # print(movie.filter_by(selection=('title', 'language'), filtering_criterion='language', filtering_value='english'))

    movie = MoviesSorted()
    s = movie.sort_by(selection=['title', 'runtime'], order_by=['runtime'], value='int')
    print(s)
    # hs = movie.highscored()
    # print(hs['Runtime'])
    # print('Runtime:', hs['Runtime'][0][0], hs['Runtime'][0][1])
    # print('Box Office:', hs['Box Office'][0][0], hs['Box Office'][0][1])
    # print('Oscars:', hs['Nominations'][0][0], hs['Nominations'][0][1])
    # print('Nominations:', hs['Nominations'][1][0], hs['Nominations'][1][1])
    # print('Awards Won:', hs['Nominations'][2][0], hs['Nominations'][2][1])
    # print('Imdb Rating:', hs['Imdb Rating'][0][0], hs['Imdb Rating'][0][1])
