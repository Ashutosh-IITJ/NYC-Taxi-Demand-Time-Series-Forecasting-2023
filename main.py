import time

# -----------------------------
# Import your pipeline modules
# -----------------------------
from download_data import download_tlc_2023_yellow
from convert_to_csv import convert_parquet_to_csv
from clean_data import clean_csv_files
from aggregate_data import aggregate_all
from visualize_data import visualize
from analyze_data import analyze

# -----------------------------
# Helper function
# -----------------------------
def banner(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

# -----------------------------
# RUN PIPELINE
# -----------------------------
def main():

    banner("STEP 1 — DOWNLOAD TLC 2023 DATA")
    download_tlc_2023_yellow(output_folder="nyc_taxi_2023")

    banner("STEP 2 — CONVERT PARQUET → CSV")
    convert_parquet_to_csv(
        input_folder="nyc_taxi_2023",
        output_folder="nyc_taxi_2023_csv"
    )

    banner("STEP 3 — CLEAN CSV DATA")
    clean_csv_files(input_folder="nyc_taxi_2023_csv")

    banner("STEP 4 — AGGREGATE ALL STATISTICS")
    aggregate_all(
        input_folder="nyc_taxi_2023_csv",
        output_folder="aggregated_outputs"
    )

    banner("STEP 5 — GENERATE VISUALIZATIONS")
    visualize()

    banner("STEP 6 — RUN SEASONAL ANALYSIS")
    analyze()

    banner("PIPELINE COMPLETE")
    print("Full annual dataset processed successfully!")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\nTotal time: {time.time() - start:.2f} seconds")
