import os
import pandas as pd
import matplotlib.pyplot as plt

def visualize():
    OUTPUT_DIR = "plots"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load aggregated files
    hourly = pd.read_csv("aggregated_outputs/hourly_trip_counts.csv")
    weekly = pd.read_csv("aggregated_outputs/weekly_trip_counts.csv")
    monthly = pd.read_csv("aggregated_outputs/monthly_trip_counts.csv")
    daily = pd.read_csv("aggregated_outputs/daily_trip_counts.csv")
    hour_weekday = pd.read_csv("aggregated_outputs/hour_weekday_matrix.csv")
    daily_stats = pd.read_csv("aggregated_outputs/daily_statistics.csv")


    # ----------------------------
    # 1. Hourly Trip Counts
    # ----------------------------
    plt.figure()
    plt.plot(hourly["hour"], hourly["trip_count"])
    plt.xlabel("Hour of Day")
    plt.ylabel("Trip Count")
    plt.title("Hourly Taxi Trip Count (24 Hours)")
    plt.grid(True)
    plt.savefig("plots/hourly_trip_count.png", dpi=300)


    # ----------------------------
    # 2. Weekly Trip Counts
    # ----------------------------
    plt.figure()
    plt.bar(weekly["weekday"], weekly["trip_count"])
    plt.xlabel("Day of Week")
    plt.ylabel("Trip Count")
    plt.title("Weekly Taxi Trip Count (Mon–Sun)")
    plt.grid(axis="y")
    plt.savefig("plots/weekly_trip_count.png", dpi=300)


    # ----------------------------
    # 3. Monthly Trip Counts
    # ----------------------------
    plt.figure()
    plt.bar(monthly["month"], monthly["trip_count"])
    plt.xlabel("Month")
    plt.ylabel("Trip Count")
    plt.title("Monthly Taxi Trip Count (Jan–Dec)")
    plt.grid(axis="y")
    plt.savefig("plots/monthly_trip_count.png", dpi=300)


    # ----------------------------
    # 4. Daily Trip Counts (Full Year)
    # ----------------------------
    daily["date"] = pd.to_datetime(daily["date"])

    plt.figure(figsize=(12, 4))
    plt.plot(daily["date"], daily["trip_count"])
    plt.xlabel("Date")
    plt.ylabel("Trip Count")
    plt.title("Daily Taxi Trip Count (Full Year)")
    plt.grid(True)
    plt.savefig("plots/daily_trip_count.png", dpi=300)


    # ----------------------------
    # 5. Hour × Weekday Heatmap Matrix
    # ----------------------------
    pivot = hour_weekday.pivot(index="hour", columns="weekday", values="trip_count")

    plt.figure(figsize=(8, 6))
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(label="Trip Count")
    plt.xlabel("Weekday (0=Mon)")
    plt.ylabel("Hour of Day")
    plt.title("Taxi Demand Heatmap: Hour × Weekday")
    plt.savefig("plots/hour_weekday_heatmap.png", dpi=300)


    # ----------------------------
    # 6. Average Daily Distance, Duration, Revenue
    # ----------------------------
    daily_stats["date"] = pd.to_datetime(daily_stats["date"])

    plt.figure(figsize=(12, 4))
    plt.plot(daily_stats["date"], daily_stats["avg_distance"])
    plt.xlabel("Date")
    plt.ylabel("Avg Distance (miles)")
    plt.title("Average Trip Distance Per Day")
    plt.grid(True)
    plt.savefig("plots/avg_distance_daily.png", dpi=300)

    plt.figure(figsize=(12, 4))
    plt.plot(daily_stats["date"], daily_stats["avg_duration_min"])
    plt.xlabel("Date")
    plt.ylabel("Avg Duration (minutes)")
    plt.title("Average Trip Duration Per Day")
    plt.grid(True)
    plt.savefig("plots/avg_duration_daily.png", dpi=300)

    plt.figure(figsize=(12, 4))
    plt.plot(daily_stats["date"], daily_stats["avg_revenue"])
    plt.xlabel("Date")
    plt.ylabel("Avg Revenue ($)")
    plt.title("Average Revenue Per Day")
    plt.grid(True)
    plt.savefig("plots/avg_revenue_daily.png", dpi=300)


    # ----------------------------
    # 7. Rolling Averages (7-day, 30-day)
    # ----------------------------
    plt.figure(figsize=(12, 4))
    plt.plot(daily_stats["date"], daily_stats["7_day_avg"], label="7-Day Avg")
    plt.plot(daily_stats["date"], daily_stats["30_day_avg"], label="30-Day Avg")
    plt.xlabel("Date")
    plt.ylabel("Revenue ($)")
    plt.title("Rolling Averages of Daily Revenue")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/rolling_averages.png", dpi=300)


    # ----------------------------
    # 8. Passenger Count (Average)
    # ----------------------------
    plt.figure(figsize=(12, 4))
    plt.plot(daily_stats["date"], daily_stats["avg_passengers"])
    plt.xlabel("Date")
    plt.ylabel("Avg Passengers")
    plt.title("Average Passengers Per Trip (Daily)")
    plt.grid(True)
    plt.savefig("plots/avg_passengers_daily.png", dpi=300)

if __name__ == '__main__':
    visualize()