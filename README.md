# Casablanca Weather Pipeline

A small Apache Airflow project that fetches a seven day hourly forecast for Casablanca from the [Open-Meteo API](https://open-meteo.com/), checks the resulting data, and upserts it into PostgreSQL.

## Pipeline

1. **Extract** hourly temperature, humidity, apparent temperature, precipitation, weather code, and wind speed.
2. **Transform** timestamps and report missing values and duplicate city/time records.
3. **Load** records into the `weather_data` table, updating existing rows for the same city and observation time.

The tasks pass records through Airflow XCom, so they do not depend on a shared local CSV file. The Postgres service is addressed as `postgres` from the Airflow containers.

## Run locally

Requirements: Docker Compose.

```bash
cp .env.example .env
```

For local use, set `AIRFLOW_UID` to your user ID on Linux. Set `FERNET_KEY` to a Fernet key (for example, generate one with `python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'`). Replace the example API JWT secret with a random value.

Build and start the services:

```bash
docker compose up -d --build
```

Open [http://localhost:8080](http://localhost:8080) and sign in with the username and password from `.env` (the example uses `airflow` / `airflow`). Find `weather_pipeline`, unpause it, and trigger a run.

Weather rows are written to the `weather_data` table in the Compose Postgres database (`airflow` by default). Set `WEATHER_DB_HOST`, `WEATHER_DB_PORT`, `WEATHER_DB_NAME`, `WEATHER_DB_USER`, and `WEATHER_DB_PASSWORD` in `.env` to change the target connection.

Stop the services with:

```bash
docker compose down
```

## Project layout

```text
.
├── dags/weather_dag.py       # Airflow DAG
├── scripts/extract.py        # Open-Meteo API extraction
├── scripts/transform.py      # Data checks and timestamp conversion
├── scripts/load.py           # PostgreSQL upsert
├── Dockerfile                # Airflow image with project dependencies
├── requirements.txt
└── docker-compose.yaml
```

## Notes

- This Compose configuration is intended for local development.
- Open-Meteo's forecast is refreshed over time; the upsert key is `(city, observation_time)`.
- The data source is Open-Meteo and the configured location is Casablanca, Morocco.
