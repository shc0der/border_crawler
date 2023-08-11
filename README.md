## Border

### Introduction
Utility for getting queue history at the border. Criteria for aggregation are set in variables in main.py
>All links pointing to the data source have been cleared.
### Installation
All variables must be registered in the .env file<br>
**BORDER_URL** - url for getting data<br>
**COOKIE_URL** - url to set up a session and set cookies<br>
**settings.py:HEADERS** - set other necessary params<br>
```console
# PROJECT
PROJECT_NAME=Border
PROJECT_VERSION=0.1

# Postgres
POSTGRES_SERVER=database
POSTGRES_USER=user
POSTGRES_PASSWORD=user
POSTGRES_DB=border_db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data/pgdata

BORDER_URL=<paste the url here>
COOKIE_URL=<paste the url here>
```


### Build & Run
To build and run the service, use docker-compose
```sh
$ docker-compose up --build
```
- PgAdmin: http://localhost:4040/

### Skeleton
```console  
.
├── app
│   ├── core            - settings
│   ├── db              - connecting to the database
│   ├── di              - di
│   ├── migrations      - migrations
│   ├── models          - models
│   │   ├── common      - common types for models
│   │   ├── domain      - database models
│   │   └── schema      - schemes
│   ├── repos           - repositories
│   │   └── dao         - dao
│   ├── workers         - workers
│   │    ├── border     - crawler for data collection
│   │    ├── common     - common classes for workers
│   │    └── parser     - parser for collected data
│   └── main.py         - entry point 
│    
├── .env                - environment variables
└── docker-compose.yml
```
### References
- docker: https://www.docker.com/
- postgresql(MIT): https://www.postgresql.org/
- sqlalchemy(MIT): https://www.sqlalchemy.org/
- alembic(MIT): https://alembic.sqlalchemy.org/
- cloudscraper(MIT): https://github.com/VeNoMouS/cloudscraper