from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from library import read_video_urls, download_video
import time


def process_csv(csv_path):
    """Process one CSV file: read its URLs and download them in parallel."""
    urls = read_video_urls(csv_path)
    print(f"Processing {csv_path} with {len(urls)} videos...")
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(download_video, urls))
    return csv_path, results


if __name__ == "__main__":
    csv_files = [
        "data/video_urls_1.csv",
        "data/video_urls_2.csv",
    ]

    start_time = time.perf_counter()
    with ThreadPoolExecutor() as threads:
        all_results = list(threads.map(process_csv, csv_files))
    nested_time = round(time.perf_counter() - start_time, 2)

    print(f"\nNested parallel time: {nested_time}s\n")

    for csv_path, results in all_results:
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "failed"]
        print(f"{csv_path}: {len(successful)} succeeded, {len(failed)} failed")
        for r in failed:
            print(f"  FAILED: {r['url']} — {r['error']}")
