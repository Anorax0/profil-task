import sys
from database_handler import MovieDB
from usage import description


def main():
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print(description)
        sys.exit()

    # this will update all movies in db
    if 'update' in sys.argv and len(sys.argv) == 2:
        movies = MovieDB()
        movies_list = movies.get_movies_list()
        movies_len = len(movies_list)
        print('Updating Movies Database. Please wait.')
        for i, movie in enumerate(movies_list):
            movies.update_movie(movie[0])
            print(f'[{i}/{movies_len}] Movie "{movie[0]}" updated.')
        print('Movies Database updated.')

    # update just one certain movie in db
    elif 'update' in sys.argv and len(sys.argv) == 3:
        movie = MovieDB()
        print(movie.update_movie(sys.argv[2]))
    else:
        print(description)
        sys.exit()


if __name__ == '__main__':
    main()
