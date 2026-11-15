
import os

import psycopg2
from psycopg2.extras import execute_values


def load_weather(df):
    # Inside Docker Compose, connect to the Postgres service by its service name.
    conn = psycopg2.connect(
        host=os.getenv("WEATHER_DB_HOST", "postgres"),
        port=os.getenv("WEATHER_DB_PORT", "5432"),
        database=os.getenv("WEATHER_DB_NAME", "airflow"),
        user=os.getenv("WEATHER_DB_USER", "airflow"),
        password=os.getenv("WEATHER_DB_PASSWORD", "airflow"),
    )

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                observation_time TIMESTAMP NOT NULL,
                city VARCHAR(100) NOT NULL,
                temperature_2m FLOAT,
                relative_humidity_2m FLOAT,
                apparent_temperature FLOAT,
                precipitation FLOAT,
                weather_code INTEGER,
                wind_speed_10m FLOAT,
                UNIQUE(city, observation_time)
            );
            """
        )

        # Prepare data
        df = df.rename(columns={"time": "observation_time"})

        columns = [
            "observation_time",
            "city",
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
        ]

        clean_df = df[columns].astype(object)
        clean_df = clean_df.where(clean_df.notna(), None)

        records = list(clean_df.itertuples(index=False, name=None))

        query = """
            INSERT INTO weather_data (
                observation_time,
                city,
                temperature_2m,
                relative_humidity_2m,
                apparent_temperature,
                precipitation,
                weather_code,
                wind_speed_10m
            )
            VALUES %s
            ON CONFLICT (city, observation_time)
            DO UPDATE SET
                temperature_2m = EXCLUDED.temperature_2m,
                relative_humidity_2m = EXCLUDED.relative_humidity_2m,
                apparent_temperature = EXCLUDED.apparent_temperature,
                precipitation = EXCLUDED.precipitation,
                weather_code = EXCLUDED.weather_code,
                wind_speed_10m = EXCLUDED.wind_speed_10m;
            """

        execute_values(cursor, query, records)

        conn.commit()

        print(f"Successfully loaded {len(records)} records!")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

