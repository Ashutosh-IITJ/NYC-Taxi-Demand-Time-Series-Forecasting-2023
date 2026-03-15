import os
import pandas as pd
import numpy as np

from datetime import datetime

US_HOLIDAYS_2023 = {
    "2023-01-01", "2023-01-16", "2023-02-20", "2023-05-29",
    "2023-06-19", "2023-07-04", "2023-09-04", "2023-10-09",
    "2023-11-11", "2023-11-23", "2023-12-25"
}

def aggregate_all(
    input_folder="nyc_taxi_2023_csv",
    output_folder="aggregated_outputs"
):
    os.makedirs(output_folder, exist_ok=True)

    hourly = {h: 0 for h in range(24)}
    weekly = {d: 0 for d in range(7)}
    monthly = {m: 0 for m in range(1, 13)}
    daily = {}
    hour_weekday = {}
    daily_stats = {}

    csv_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".csv")])
    print(f"Found {len(csv_files)} files.\n")

    for file in csv_files:
        print(f"Processing: {file}")
        path = os.path.join(input_folder, file)

        for chunk in pd.read_csv(
            path,
            chunksize=100_000,
            usecols=[
                "tpep_pickup_datetime", "tpep_dropoff_datetime",
                "trip_distance", "total_amount",
                "passenger_count"
            ]
        ):
            chunk["pickup"] = pd.to_datetime(chunk["tpep_pickup_datetime"], errors="coerce")
            chunk["dropoff"] = pd.to_datetime(chunk["tpep_dropoff_datetime"], errors="coerce")
            chunk.dropna(subset=["pickup", "dropoff"], inplace=True)
            chunk["hour"] = chunk["pickup"].dt.hour
            chunk["weekday"] = chunk["pickup"].dt.weekday
            chunk["month"] = chunk["pickup"].dt.month
            chunk["date"] = chunk["pickup"].dt.date
            chunk["duration_min"] = (chunk["dropoff"] - chunk["pickup"]).dt.total_seconds() / 60

            hour_counts = chunk["hour"].value_counts()
            for h, c in hour_counts.items():
                hourly[int(h)] += int(c)

            week_counts = chunk["weekday"].value_counts()
            for d, c in week_counts.items():
                weekly[int(d)] += int(c)

            month_counts = chunk["month"].value_counts()
            for m, c in month_counts.items():
                monthly[int(m)] += int(c)

            date_counts = chunk["date"].value_counts()
            for dt, c in date_counts.items():
                daily[dt] = daily.get(dt, 0) + int(c)

            group_hw = chunk.groupby(["hour", "weekday"]).size()
            for (h, d), c in group_hw.items():
                hour_weekday[(int(h), int(d))] = hour_weekday.get((int(h), int(d)), 0) + int(c)

            for dt, g in chunk.groupby("date"):

                if dt not in daily_stats:
                    daily_stats[dt] = {
                        "total_distance": 0,
                        "total_duration": 0,
                        "total_revenue": 0,
                        "total_passengers": 0,
                        "trip_count": 0
                    }

                daily_stats[dt]["total_distance"] += g["trip_distance"].sum()
                daily_stats[dt]["total_duration"] += g["duration_min"].sum()
                daily_stats[dt]["total_revenue"] += g["total_amount"].sum()
                daily_stats[dt]["total_passengers"] += g["passenger_count"].sum()
                daily_stats[dt]["trip_count"] += len(g)

    pd.DataFrame({"hour": list(hourly.keys()), "trip_count": list(hourly.values())}) \
        .to_csv(f"{output_folder}/hourly_trip_counts.csv", index=False)

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pd.DataFrame({
        "weekday": day_names,
        "trip_count": [weekly[i] for i in range(7)]
    }).to_csv(f"{output_folder}/weekly_trip_counts.csv", index=False)

    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    pd.DataFrame({
        "month": month_names,
        "trip_count": [monthly[m] for m in range(1, 13)]
    }).to_csv(f"{output_folder}/monthly_trip_counts.csv", index=False)

    df_daily = pd.DataFrame(sorted(daily.items()), columns=["date", "trip_count"])
    df_daily.to_csv(f"{output_folder}/daily_trip_counts.csv", index=False)

    df_hw = pd.DataFrame([
        {"hour": h, "weekday": d, "trip_count": c}
        for (h, d), c in hour_weekday.items()
    ])
    df_hw.to_csv(f"{output_folder}/hour_weekday_matrix.csv", index=False)

    stats_rows = []
    for dt, v in sorted(daily_stats.items()):
        stats_rows.append({
            "date": dt,
            "avg_distance": v["total_distance"] / v["trip_count"],
            "avg_duration_min": v["total_duration"] / v["trip_count"],
            "avg_revenue": v["total_revenue"] / v["trip_count"],
            "avg_passengers": v["total_passengers"] / v["trip_count"],
        })

    df_stats = pd.DataFrame(stats_rows)

    df_stats["holiday"] = df_stats["date"].astype(str).isin(US_HOLIDAYS_2023).astype(int)
    df_stats["7_day_avg"] = df_stats["avg_revenue"].rolling(7).mean()
    df_stats["30_day_avg"] = df_stats["avg_revenue"].rolling(30).mean()

    df_stats.to_csv(f"{output_folder}/daily_statistics.csv", index=False)

if __name__ == "__main__":
    aggregate_all()
