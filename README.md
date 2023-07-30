[![Website iafpa-db.ch](https://img.shields.io/website-up-down-green-red/http/flamberg-tschugger.ch.svg)](https://flamberg-tschugger.ch)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/alexarnimueller/iafpa-app)
[![Maintainer](https://img.shields.io/badge/maintainer-alexarnimueller-blue)](https://github.com/alexarnimueller)

# Portal für APV Aktivitas Tschugger Tag

## Initialization

To initialize the application and its database, run the following

```
# set up the SSL certificates using certbot
bash init-letsencrypt.sh
```

To initialize the database once, connect to the running DB container as follows:

```
docker exec -it tschugger_db_1 psql -U postgres
```

Then, create the user and DB:

```
CREATE USER tschugger;
CREATE DATABASE tschugger;
GRANT ALL PRIVILEGES ON tschugger TO tschugger;
```

## Run

After initialization the application is already running. If you make changes to the code and would like to rebuild and run the app, do

```
# shut down
docker-compose down

# rebuild and run
docker-compose up --build -d
```

The app is then running again with the changes.
