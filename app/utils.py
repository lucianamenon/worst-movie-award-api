import pandas as pd
from app.models import db, Movie, Producer, MovieProducer

def populate_tables(csv_path):

    """Populate movies, producers and movieProduces tables based on data of MOVIES_DATA_PATH (configuration file on app/config/settings.py)"""

    imported_rows = 0
    imported_producers = 0

    Movie.delete_all()
    Producer.delete_all()
    MovieProducer.delete_all()

    csv_file = pd.read_csv(csv_path, delimiter=";")

    for i, row in csv_file.iterrows():

        movie = Movie(
            id=i+1,
            year=row["year"],
            title=row["title"],
            studios=row["studios"],
            producers=row["producers"],
            winner=True if row["winner"] == "yes" else False
        )
        Movie.insert(movie)

        for name in [x.strip() for x in row["producers"].replace(', and ', ',').replace(' and ', ',').split(',')]:
            producer_id = Producer.get_producer(name)
            if not producer_id:
                imported_producers += 1
                producer_id = imported_producers
                producer = Producer(id=imported_producers, producer=name)
                Producer.insert(producer)

            movie_producers = MovieProducer(movie.id, producer_id)
            MovieProducer.insert(movie_producers)

        imported_rows += 1

    db.session.commit()
    print(f"\nData loading complete! Imported {imported_rows} movies. Imported {imported_producers} different producers.\n")

def get_min_max_interval():

    movie_producers = {}
    for item in MovieProducer.get_producer_winners():
        if not item.producer_name in movie_producers:
            movie_producers[item.producer_name] = [item.movie_year]
        else:
            years_list = movie_producers[item.producer_name]
            years_list.append(item.movie_year)
            movie_producers[item.producer_name] = years_list

    all_intervals = []
    for item in movie_producers:
        years_list = movie_producers[item]
        #ignore produces that won only once
        if len(years_list) == 1:
            continue
        for i in range(len(years_list)-1):
            interval = {}
            interval["producer"] = item
            interval["interval"] = years_list[i+1] - years_list[i]
            interval["previousWin"] = years_list[i]
            interval["followingWin"] = years_list[i+1]
            all_intervals.append(interval)

    list_max_interval, list_min_interval = [], []
    max_interval = max(all_intervals, key=lambda x:x['interval'])['interval']
    min_interval = min(all_intervals, key=lambda x:x['interval'])['interval']
    for item in all_intervals:
        if item['interval'] == max_interval:
            list_max_interval.append(item)
        if item['interval'] == min_interval:
            list_min_interval.append(item)

    return {"min": list_min_interval, "max": list_max_interval}
