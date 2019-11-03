description = """
--- Help ---

Type --help or -h to show this again.

Type "clean" to clean database - this is necessary before first use.

Type "update movie-title" to update records in database for specific movie.
Example: update "American Beauty"

Type "update" to update all records in database (db must be cleaned).

Type "--sort_by [options]" to sort movies by given criterions .
[options: every db column name, can add integer at end to specify query limit]
Example: --sort_by year runtime 20

Type "--filter_by [criterion] [value looking for]" to received filtered records from database.
[criterion: db column name; value]
Example: --filter_by language Spanish
Example: --filter_by director Lasseter

Type "--highscores" or "-hs" to retrieve top records in Runtime, Box Office, Oscars, Nominations,
 Awards Won, and Imdb Rating category.
 
Type "--compare [criterion] [first title] [second title]" to compare two movies in specific category.
Example: --compare runtime "Joker" "Die Hard"

Type "--add [movie title]" to add specific movie to database.

"""