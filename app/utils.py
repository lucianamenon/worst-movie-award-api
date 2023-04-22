import pandas as pd
from app.models import Movie, Producer, MovieProducer

def populate_tables(csv_path):

    """Populate movies, producers and movieProduces tables based on data of MOVIES_DATA_PATH (configuration file on app/config/settings.py)"""

    imported_rows = 0
    imported_producers = 0

    Movie.delete_all()
    Producer.delete_all()
    MovieProducer.delete_all()

    csv_file = pd.read_csv(csv_path, delimiter=";")

    for _, row in csv_file.iterrows():

        movie = Movie(
            year=row["year"],
            title=row["title"],
            studios=row["studios"],
            producers=row["producers"],
            winner=True if row["winner"] == "yes" else False
        )
        Movie.insert(movie)
        print(Movie.json(movie))

        for name in [x.strip() for x in row["producers"].replace(', and ', ',').replace(' and ', ',').split(',')]:
            producer_id = Producer.get_producer(name)
            if not producer_id:
                producer = Producer(producer=name)
                Producer.insert(producer)
                imported_producers += 1
                producer_id = producer.id

            movie_producers = MovieProducer(movie.id, producer_id)
            MovieProducer.insert(movie_producers)

        imported_rows += 1

    print(f"Data loading complete! Imported {imported_rows} movies. Imported {imported_producers} different producers. ")
