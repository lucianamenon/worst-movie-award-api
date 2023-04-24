
# TEXO IT - Worst Movie Award API

## About The Project
REST API to read the list of nominees and winners of the Worst Film category of the Golden Raspberry Awards from a CSV data source, store the data into an in-memory database and return the producer with the longest interval between two awards, and the one who got two awards faster.

### Important notes

This api takes into account each producer when querying the minimum and maximum interval between two awards, even if the movie was produced in group. (Example: Producer Joel Silver was nominated alone in the year 1989 and the following year he is nominated again, but this time with Steven Perry, when processing Joel Silver this API considers both nominations.

### API Endpoint

**GET /api/v1/texo/producers-award-interval**

Returns producers with maximum and minimum interval between two awards.

**Response sample:**
```
{
    "max": [
        {
            "followingWin": 2015,
            "interval": 13,
            "previousWin": 2002,
            "producer": "Matthew Vaughn"
        }
    ],
    "min": [
        {
            "followingWin": 1991,
            "interval": 1,
            "previousWin": 1990,
            "producer": "Joel Silver"
        }
    ]
}
```

### Other Endpoints
  + `GET /api/v1/texo/movies` - Returns all movies list
  + `GET /api/v1/texo/producers` - Returns all producers list
  + `GET /api/v1/texo/check` - Check if the application is running


## Installation and Tests

### Local run

+ Clone the repo, set an python 3 virtual environment, install the dependencies from requirementes.txt and run the project:

```
  python main.py
```
The service will run on port 5000.

```
  curl http://localhost:5000/api/v1/texo/producers-award-interval
```

To run tests, be in root directory and run:

```
  python -m unittest
```

### Docker run

+ If you don't want to worry about the dependencies, you can run it via Docker, inside the repository folder, run:

```
  docker build -t docker_worst_movie_api:latest .
  docker stop docker_worst_movie_api
  docker rm docker_worst_movie_api

  docker run -t -p $PORT:5000 --restart=always --name=docker_worst_movie_api docker_worst_movie_api:latest
```
The service will run on port $PORT.

```
  curl http://localhost:$PORT/api/v1/texo/producers-award-interval
```

### Custom CSV file

To use another CSV data source change the configuration file (app/config/settings.py) and **rerun the application**.

```
  MOVIES_DATA_PATH = "your-movielist-path.csv"
```

Remember that the CSV file must have the structure below:

```
  year;title;studios;producers;winner
  1980;Movie Title 1;Studio 1;Producer 1;
  1981;Movie Title 2;Studio 2;Producer 2;
  1982;Movie Title 3;Studio 3;Producer 3;yes
```

## Contact

* E-mail : trinkaus.luciana@gmail.com
* Linkedin: https://www.linkedin.com/in/luciana-menon/