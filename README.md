# NYC Taxi Demand Time Series Forecasting (2023)

End-to-end pipeline for NYC Yellow Taxi data:
- download monthly 2023 trip data
- convert Parquet to CSV
- clean and aggregate demand metrics
- visualize patterns
- run STL + ACF/PACF + SARIMA analysis

## Data Sources

Official NYC TLC trip-record page:
- https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Direct hosted files (used by the downloader):
- Base URL: `https://d37ci6vzurychx.cloudfront.net/trip-data/`
- File pattern: `yellow_tripdata_2023-<MM>.parquet`
- Example: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet

## Requirements

- Python 3.9+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Full Pipeline

```bash
python main.py
```

Pipeline stages:
1. Download raw Parquet files
2. Convert Parquet to CSV
3. Clean CSV files
4. Aggregate daily/weekly/monthly/hourly metrics
5. Generate plots
6. Run seasonal time-series analysis

## Project Structure

```text
.
├── main.py
├── download_data.py
├── convert_to_csv.py
├── clean_data.py
├── aggregate_data.py
├── visualize_data.py
├── analyze_data.py
├── requirements.txt
├── README.md
├── .gitignore
├── nyc_taxi_2023/        # generated raw parquet files (ignored)
├── nyc_taxi_2023_csv/    # generated CSV files (ignored)
├── aggregated_outputs/   # generated aggregates (ignored)
├── plots/                # generated plots (ignored)
└── results/              # generated model outputs (ignored)
```

## Notes for GitHub

This repo is configured to avoid committing large generated data/output folders.

If you want to regenerate everything from scratch:
1. Keep only code files and `requirements.txt`
2. Run `python main.py`
3. Outputs will be recreated locally
