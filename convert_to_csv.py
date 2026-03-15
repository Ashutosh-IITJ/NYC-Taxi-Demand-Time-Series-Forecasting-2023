import os
import pyarrow.parquet as pq
import pyarrow.csv as pc

def convert_parquet_to_csv(input_folder="nyc_taxi_2023", output_folder="nyc_taxi_2023_csv"):
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.endswith(".parquet")]

    for file in files:
        parquet_path = os.path.join(input_folder, file)
        csv_file = file.replace(".parquet", ".csv")
        csv_path = os.path.join(output_folder, csv_file)

        table = pq.read_table(parquet_path)

        pc.write_csv(table, csv_path)

if __name__ == "__main__":
    convert_parquet_to_csv()
