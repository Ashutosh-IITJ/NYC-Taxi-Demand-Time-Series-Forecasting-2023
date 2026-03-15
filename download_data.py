import os
import requests
from tqdm import tqdm

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    
    if response.status_code != 200:
        return
    
    total_size = int(response.headers.get("content-length", 0))
    block_size = 8192
    
    with open(output_path, "wb") as file, tqdm(
        total=total_size,
        unit="B",
        unit_scale=True,
        desc=os.path.basename(output_path),
        ncols=80
    ) as pbar:
        for data in response.iter_content(block_size):
            file.write(data)
            pbar.update(len(data))


def download_tlc_2023_yellow(output_folder="nyc_taxi_2023"):
    os.makedirs(output_folder, exist_ok=True)

    for month in range(1, 13):
        month_str = f"{month:02d}"
        file_name = f"yellow_tripdata_2023-{month_str}.parquet"
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
        output_path = os.path.join(output_folder, file_name)

        print(f"Downloading {file_name}...")
        download_file(url, output_path)

if __name__ == "__main__":
    download_tlc_2023_yellow()
