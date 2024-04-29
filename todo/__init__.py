__app_name__ = "cli-todo"
__version__ = "0.0.1"
__author__ = 'Nanda Gopal Pattanayak'

(
    SUCCESS,
    DIRECTORY_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIRECTORY_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}