import sys
from update_db import update_movie
from omdb import get_movie_data
from file_usage import file_usage


def main():
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print(file_usage)

    if 'update' in sys.argv and len(sys.argv) == 2:
        pass
    elif 'update' in sys.argv and isinstance(sys.argv[2], str) and len(sys.argv) == 3:
        update_movie(sys.argv[2])
    else:
        print(file_usage)


if __name__ == '__main__':
    main()
