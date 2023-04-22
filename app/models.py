from app.database import db

class Movie(db.Model):

    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    studios = db.Column(db.String, nullable=False)
    producers = db.Column(db.String, nullable=False)
    winner = db.Column(db.Boolean, default=False)

    def __init__(self, id, year, title, studios, producers, winner):
        self.id = id
        self.year = year
        self.title = title
        self.studios = studios
        self.producers = producers
        self.winner = winner

    def json(self):
        return {'id': self.id, 'year': self.year, 'title': self.title, 'studios': self.studios, 'producers': self.producers, 'winner': self.winner}

    @classmethod
    def get_all(cls):
        result = db.engine.execute("SELECT * FROM movies")
        rows = result.fetchall()
        movies = []
        for item in rows:
            movies.append(cls.json(item))
        return movies

    @classmethod
    def delete_all(cls) -> None:
        cls.query.delete()

    def insert(self) -> None:
        db.session.add(self)


class Producer(db.Model):
    __tablename__ = "producers"
    id = db.Column(db.Integer, primary_key=True)
    producer = db.Column(db.String, nullable=False)

    def __init__(self, id, producer):
        self.id = id
        self.producer = producer

    def json(self):
        return {'id': self.id, 'producer': self.producer}

    @classmethod
    def get_all(cls):
        result = db.engine.execute("SELECT * FROM producers")
        rows = result.fetchall()
        producers = []
        for item in rows:
            producers.append(cls.json(item))
        return producers

    @classmethod
    def get_producer(cls, producer_name):
        result = db.engine.execute(f"""SELECT id FROM producers where producer = '{producer_name}'""")
        rows = result.fetchone()
        producer_id = ""
        if rows:
            producer_id = rows['id']
        return producer_id

    @classmethod
    def delete_all(cls) -> None:
        cls.query.delete()

    def insert(self) -> None:
        db.session.add(self)

class MovieProducer(db.Model):
    __tablename__ = "movieProducers"
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey("producers.id"), primary_key=True)

    def __init__(self, movie_id, producer_id):
        self.movie_id = movie_id
        self.producer_id = producer_id

    @classmethod
    def get_producer_winners(cls):
        result = db.engine.execute(
            """SELECT producers.producer AS producer_name, movies.year AS movie_year
                FROM movieProducers
                    INNER JOIN movies ON movies.id = movieProducers.movie_id
                    INNER JOIN producers ON producers.id = movieProducers.producer_id
                WHERE movies.winner ORDER BY producer_name, movie_year"""
        )
        return result

    @classmethod
    def delete_all(cls) -> None:
        cls.query.delete()

    def insert(self) -> None:
        db.session.add(self)
