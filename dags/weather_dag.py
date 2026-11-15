from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False
)
def weather_pipeline():

    @task
    def extract():
        from scripts.extract import extract_weather

        df = extract_weather()
        return df.to_dict(orient="records")

    @task
    def transform(records):
        import pandas as pd
        from scripts.transform import transform_weather

        df = transform_weather(pd.DataFrame.from_records(records))
        df["time"] = df["time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
        return df.to_dict(orient="records")

    @task
    def load(records):
        import pandas as pd
        from scripts.load import load_weather

        load_weather(pd.DataFrame.from_records(records))

    extracted_records = extract()
    transformed_records = transform(extracted_records)
    load_task = load(transformed_records)



weather_pipeline()
