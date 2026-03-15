import os
import pandas as pd

def clean_csv_files(input_folder="nyc_taxi_2023_csv"):
    csv_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".csv")])

    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        temp_path = file_path + ".tmp"

        print(f"Cleaning: {file}")

        if os.path.exists(temp_path):
            os.remove(temp_path)

        for chunk in pd.read_csv(file_path, chunksize=100_000):
            chunk = chunk.dropna()

            chunk.to_csv(
                temp_path,
                mode='a',
                index=False,
                header=not os.path.exists(temp_path)
            )

        os.remove(file_path)
        os.rename(temp_path, file_path)

        print(f"✔ Cleaned {file}")

    print("\n✔ All CSV files cleaned successfully!")


if __name__ == "__main__":
    clean_csv_files()
