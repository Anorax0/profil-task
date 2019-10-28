import sys
from database_handler import MovieDB, MoviesSorted
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

    # This is needed due to extra spaces in titles in DB, which made querying quite difficult
    elif 'clean' in sys.argv:
        cleaning = MovieDB()
        cleaning.clean()
        print('Database cleaned.')

    # update just one certain movie in db
    elif 'update' in sys.argv and len(sys.argv) == 3:
        movie = MovieDB()
        print(movie.update_movie(sys.argv[2]))

    elif '--sort_by' in sys.argv or '-s' in sys.argv:
        movies = MoviesSorted()
        limit = 10
        order_way = 'DESC'
        selection = (", ".join([str(x) for x in sys.argv[2:] if not x.isdigit()])).lower()
        if sys.argv[-1].isdigit():
            limit = int(sys.argv[-1])
        print('----', selection)

        sorted_movies_list = movies.sort_by(selection=['title', selection],
                                            order_by=[selection],
                                            query_limit=limit)
        for sorted_movie in sorted_movies_list:
            print(sorted_movie)

    elif '--highscores' in sys.argv or '-hs' in sys.argv:
        movies = MoviesSorted()
        highscored_list = movies.highscored()
        for highscored in highscored_list:
            print('{}: {} - {}'.format(highscored[0], highscored[1][0][0], highscored[1][0][1]))

    else:
        print(description)
        sys.exit()


if __name__ == '__main__':
    main()
