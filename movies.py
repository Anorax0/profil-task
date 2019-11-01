import sys
from database_handler import MovieDB, MoviesSorted
from usage import description


def main():
    options = ('title', 'year', 'runtime', 'genre', 'director', 'cast', 'writer', 'language',
               'country', 'awards', 'imdb_rating', 'imdb_votes', 'box_office')

    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print(description)
        sys.exit()

    if 'update' in sys.argv:
        # update just one certain movie in db
        if len(sys.argv) == 3:
            movie = MovieDB()
            print(movie.update_movie(sys.argv[2]))
            sys.exit()

        # this will update all movies in db
        movies = MovieDB()
        movies_list = movies.get_movies_list()
        movies_len = len(movies_list)
        print('Updating Movies Database. Please wait.')
        for i, movie in enumerate(movies_list):
            certain_movie = MovieDB()
            certain_movie.update_movie(movie[0])
            del certain_movie
            print(f'[{i}/{movies_len}] Movie "{movie[0]}" updated.')
        print('Movies Database updated.')

    # This is needed due to extra spaces in titles in DB, which made querying quite difficult
    elif 'clean' in sys.argv:
        cleaning = MovieDB()
        cleaning.clean()
        print('Database cleaned.')

    elif '--sort_by' in sys.argv or '-s' in sys.argv:
        if len(sys.argv) < 3:
            print('Incorrect amount of given arguments.')
            sys.exit()
        movies = MoviesSorted()
        limit = 10
        selection = (", ".join([str(x) for x in sys.argv[2:] if not x.isdigit()])).lower()
        if sys.argv[-1].isdigit():
            limit = int(sys.argv[-1])

        sorted_movies_list = movies.sort_by(selection=['title', selection],
                                            order_by=[selection],
                                            query_limit=limit)
        for sorted_movie in sorted_movies_list:
            print(sorted_movie)

    elif '--filter_by' in sys.argv:
        if len(sys.argv) < 4:
            print('Please provide 2 arguments: filtering category and value you are looking for.')
            sys.exit()
        if sys.argv[-1].isdigit():
            query_limit = sys.argv[-1]
        movies = MoviesSorted()
        filtered_movies = movies.filter_by(selection=('title', sys.argv[2]),
                                           filtering_criterion=sys.argv[2],
                                           filtering_value=sys.argv[3],
                                           query_limit=query_limit)
        for fil_mov in filtered_movies:
            print(fil_mov[0]+':', fil_mov[1])

    elif '--highscores' in sys.argv or '-hs' in sys.argv:
        movies = MoviesSorted()
        highscored = movies.highscored()

        print('Runtime:', highscored['Runtime'][0], str(highscored['Runtime'][1])+'m')
        print('Box Office:', highscored['Box Office'][0][0], '$'+str(format(highscored['Box Office'][0][1], ",")))
        print('Oscars:', highscored['Nominations'][0][0], highscored['Nominations'][0][1])
        print('Nominations:', highscored['Nominations'][1][0], highscored['Nominations'][1][1])
        print('Awards Won:', highscored['Nominations'][2][0], highscored['Nominations'][2][1])
        print('Imdb Rating:', highscored['Imdb Rating'][0][0], str(highscored['Imdb Rating'][0][1])+'/10')

    elif '--compare' in sys.argv:
        if len(sys.argv) != 5:
            print('Incorrect amount of given arguments.')
            sys.exit()
        if sys.argv[2] in options:
            movies = MoviesSorted()
            compare_movies = movies.compare(comparing_criterion=sys.argv[2],
                                            comparing_values=(sys.argv[3], sys.argv[4]))

    else:
        print(description)
        sys.exit()


if __name__ == '__main__':
    main()
