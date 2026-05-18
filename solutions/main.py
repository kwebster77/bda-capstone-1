from library import download_video, read_video_urls, create_report
import time
from multiprocessing import Pool


if __name__ == "__main__":
    urls = read_video_urls("data/video_urls.csv")

    # Sequential processing
    start_time = time.perf_counter()
    for url in urls:
        download_video(url)
    sequential_time = round(time.perf_counter() - start_time, 2)
    print(f"Sequential time: {sequential_time}s")

    # Parallel processing
    with Pool() as pool:
        start_time = time.perf_counter()
        pool.map(download_video, urls)
    parallel_time = round(time.perf_counter() - start_time, 2)
    print(f"Parallel time: {parallel_time}s")

    create_report(sequential_time, parallel_time, len(urls))