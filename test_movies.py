import pytest

from database_handler import Movies, MovieDB, MoviesSorted
from omdb import get_movie_data


def test_movie_init():
    test_movie = Movies()

    assert test_movie.title is None, "test failed"
    assert test_movie.runtime is None, "test failed"


def test_connection():
    test_movie = Movies()
    test_movie._open()
    get_first_movie = test_movie.c.execute("SELECT * FROM movies WHERE id=0").fetchone()
    assert "The Shawshank Redemption" in get_first_movie, 'test failed'
    test_movie._close()


def test_movie_from_db():
    test_movie = MovieDB()
    test_movie.get_movie_from_db('Oldboy')
    assert test_movie.title == 'Oldboy', 'test failed'
    assert int(test_movie.year) == 2003, 'test failed'
    assert int(test_movie.runtime) == 120, 'test failed'
    assert test_movie.genre == 'Action, Drama, Mystery, Thriller', 'test failed'
    assert test_movie.director == 'Chan-wook Park', 'test failed'
    assert test_movie.cast == 'Min-sik Choi, Ji-tae Yu, Hye-jeong Kang, Dae-han Ji', 'test failed'
    assert test_movie.writer == 'Garon Tsuchiya (story), Nobuaki Minegishi (comic), Chan-wook Park (character created' \
                                ' by: Oldboy,  Vengeance Trilogy), Chan-wook Park (screenplay), Joon-hyung Lim ' \
                                '(screenplay), Jo-yun Hwang (screenplay)', 'test failed'
    assert test_movie.language == 'Korean', 'test failed'
    assert test_movie.country == 'South Korea', 'test failed'
    assert test_movie.awards == '38 wins & 18 nominations.', 'test failed'
    assert float(test_movie.imdb_rating) == 8.4, 'test failed'
    assert int(test_movie.imdb_votes) == 468285, 'test failed'
    assert int(test_movie.box_office) == 637778, 'test failed'
    del test_movie
    test_movie = MovieDB()
    assert test_movie.title is None, 'test failed'


def test_all_movies_list():
    test_movie = Movies()
    test_movie._open()
    movies_list = test_movie.get_movies_list()
    assert len(movies_list) == 100, 'test failed'
    test_movie._close()


def test_sort_by():
    test_movie = MoviesSorted()
    sorted_movies = test_movie.sort_by(selection=('title', 'year'), order_by=('year', ), query_limit=1)
    assert sorted_movies == [('Joker', 2019)], 'test failed'


def test_highscores():
    test_movie = MoviesSorted()
    highscores = test_movie.highscored()
    assert highscores['Runtime'][0] == 'Gone with the Wind', 'test failed'
    assert int(highscores['Runtime'][1]) == 238, 'test failed'
    assert highscores['Box Office'][0][0] == 'The Dark Knight', 'test failed'
    assert int(highscores['Box Office'][0][1]) == 533316061, 'test failed'
    assert highscores['Nominations'][0][0] == 'Amadeus', 'test failed'
    assert int(highscores['Nominations'][0][1]) == 8, 'test failed'
    assert highscores['Nominations'][1][0] == 'Inception', 'test failed'
    assert int(highscores['Nominations'][1][1]) == 204, 'test failed'
    assert highscores['Nominations'][2][0] == 'No Country for Old Men', 'test failed'
    assert int(highscores['Nominations'][2][1]) == 157, 'test failed'
    assert highscores['Imdb Rating'][0][0] == 'The Shawshank Redemption', 'test failed'
    assert float(highscores['Imdb Rating'][0][1]) == 9.3, 'test failed'


def test_top_runtime():
    test_movie = MoviesSorted()
    top_runtime = test_movie.get_top_runtime()
    assert int(top_runtime[1]) == 238, 'test failed'


def test_filter_by():
    test_movie = MoviesSorted()
    filter_movie = test_movie.filter_by(selection=('title', 'director'),
                                        filtering_criterion='director',
                                        filtering_value='Lasseter',
                                        query_limit=1)
    assert filter_movie[0][0] == 'Toy Story', 'test failed'
    assert filter_movie[0][1] == 'John Lasseter', 'test failed'


def test_compare():
    test_movie = MoviesSorted()
    compare_movies1 = test_movie.compare(comparing_criterion='box_office',
                                         comparing_values=("Coco", "Inception"))
    compare_movies2 = test_movie.compare(comparing_criterion='runtime',
                                         comparing_values=("Joker", "Die Hard"))
    assert compare_movies1 == 'Box_Office of Coco is smaller than box_office of Inception [208487719 < 292568851]',\
        'test failed'
    assert compare_movies2 == 'Runtime of Joker is smaller than runtime of Die Hard [122 < 132]', 'test failed'


def test_not_existing_movie():
    test_movie = MovieDB()
    test_movie.get_movie_from_db('Hellboy')
    assert test_movie.title is None, 'test failed'


def test_add_movie():
    test_movie = MovieDB()
    test_movie.add_movie('Hellboy')
    assert test_movie.title == 'Hellboy', 'test failed'
    assert int(test_movie.year) == 2004, 'test failed'
    test_movie._open()
    test_movie.c.execute("DELETE FROM movies WHERE title='Hellboy'")
    test_movie._close()
