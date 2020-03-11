import pytest

from database_handler import Movies, MovieDB, MoviesSorted
from omdb import get_movie_data


@pytest.fixture()
def movies_class():
    test_movie = Movies()
    test_movie._open()
    # get_first_movie = test_movie.c.execute("SELECT * FROM movies WHERE id=0").fetchone()
    # assert "The Shawshank Redemption" in get_first_movie, 'test failed'
    yield test_movie
    test_movie._close()


@pytest.fixture()
def movies_db_class():
    movie = MovieDB()
    return movie


@pytest.fixture()
def movies_sorted_class():
    movie = MoviesSorted()
    yield movie


def test_movie_init(movies_class):
    # test_movie = Movies()

    assert movies_class.title is None, "test failed"
    assert movies_class.runtime is None, "test failed"


def test_empty_movie_db(movies_class):
    assert str(movies_class) == 'None, None'


def test_first_movie(movies_class):
    get_first_movie = movies_class.c.execute("SELECT * FROM movies WHERE id=0").fetchone()
    assert "The Shawshank Redemption" in get_first_movie, 'test failed'


def test_movie_from_db(movies_db_class):
    movies_db_class.get_movie_from_db('Oldboy')
    assert movies_db_class.title == 'Oldboy', 'test failed'
    assert int(movies_db_class.year) == 2003, 'test failed'
    assert int(movies_db_class.runtime) == 120, 'test failed'
    assert movies_db_class.genre == 'Action, Drama, Mystery, Thriller', 'test failed'
    assert movies_db_class.director == 'Chan-wook Park', 'test failed'
    assert movies_db_class.cast == 'Min-sik Choi, Ji-Tae Yoo, Hye-jeong Kang, Dae-han Ji', 'test failed'
    assert movies_db_class.writer == 'Garon Tsuchiya (story), Nobuaki Minegishi (comic), Chan-wook Park (character created' \
                                ' by: Oldboy,  Vengeance Trilogy), Chan-wook Park (screenplay), Joon-hyung Lim ' \
                                '(screenplay), Jo-yun Hwang (screenplay)', 'test failed'
    assert movies_db_class.language == 'Korean', 'test failed'
    assert movies_db_class.country == 'South Korea', 'test failed'
    assert movies_db_class.awards == '39 wins & 18 nominations.', 'test failed'
    assert float(movies_db_class.imdb_rating) == 8.4, 'test failed'
    assert int(movies_db_class.imdb_votes) == 478667, 'test failed'
    assert int(movies_db_class.box_office) == 637778, 'test failed'
    del movies_db_class
    test_movie = MovieDB()
    assert test_movie.title is None, 'test failed'


def test_all_movies_list(movies_class):
    movies_list = movies_class.get_movies_list()
    assert len(movies_list) == 100, 'test failed'


def test_sort_by(movies_sorted_class):
    sorted_movies = movies_sorted_class.sort_by(selection=('title', 'year'), order_by=('year', ), query_limit=1)
    assert sorted_movies == [('Joker', 2019)], 'test failed'


def test_highscores(movies_sorted_class):
    highscores = movies_sorted_class.highscored()
    assert highscores['Runtime'][0] == 'Gone with the Wind', 'test failed'
    assert int(highscores['Runtime'][1]) == 238, 'test failed'
    assert highscores['Box Office'][0][0] == 'The Dark Knight', 'test failed'
    assert int(highscores['Box Office'][0][1]) == 533316061, 'test failed'
    assert highscores['Nominations'][0][0] == 'Amadeus', 'test failed'
    assert int(highscores['Nominations'][0][1]) == 8, 'test failed'
    assert highscores['Nominations'][1][0] == 'Parasite', 'test failed'
    assert int(highscores['Nominations'][1][1]) == 231, 'test failed'
    assert highscores['Nominations'][2][0] == 'Parasite', 'test failed'
    assert int(highscores['Nominations'][2][1]) == 241, 'test failed'
    assert highscores['Imdb Rating'][0][0] == 'The Shawshank Redemption', 'test failed'
    assert float(highscores['Imdb Rating'][0][1]) == 9.3, 'test failed'


def test_top_runtime(movies_sorted_class):
    top_runtime = movies_sorted_class.get_top_runtime()
    assert int(top_runtime[1]) == 238, 'test failed'


def test_filter_by(movies_sorted_class):
    filter_movie = movies_sorted_class.filter_by(selection=('title', 'director'),
                                        filtering_criterion='director',
                                        filtering_value='Lasseter',
                                        query_limit=1)
    assert filter_movie[0][0] == 'Toy Story', 'test failed'
    assert filter_movie[0][1] == 'John Lasseter', 'test failed'


def test_compare(movies_sorted_class):
    compare_movies = movies_sorted_class.compare(comparing_criterion='runtime',
                                                 comparing_values=("Joker", "Die Hard"))
    assert compare_movies == 'Runtime of Joker is smaller than runtime of Die Hard [122 < 132]', 'test failed'


def test_not_existing_movie(movies_db_class):
    movies_db_class.get_movie_from_db()
    assert movies_db_class.title is None, 'test failed'


# def test_add_movie(movies_db_class):
#     movies_db_class.add_movie('Hellboy')
#     assert movies_db_class.title == 'Hellboy', 'test failed'
#     # assert int(movies_db_class.year) == 2004, 'test failed'
#     movies_db_class._open()
#     movies_db_class.c.execute("DELETE FROM movies WHERE title='Hellboy'")
#     movies_db_class._close()
