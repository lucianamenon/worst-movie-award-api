class BaseConfig():
    DATABASE_NAME = "worst_movie_award"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_NAME}.db"
    MOVIES_DATA_PATH = "movielist.csv"