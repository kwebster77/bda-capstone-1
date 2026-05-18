from library import download_video, read_video_urls, create_report
import time
from multiprocessing import Pool



if __name__ == "__main__":
    # start_time = time.perf_counter()
    # urls = read_video_urls("data/video_urls.csv")
    # print("video urls:", urls)
    # for url in urls:
    #     download_video(url)
    #     print(f"Download time for {url}: {time.perf_counter() - start_time} seconds")
    # end_time = time.perf_counter()
    # total_time = end_time - start_time
    # create_report(round(total_time, 2))
    with Pool() as pool:
        start_time = time.perf_counter()
        results = pool.map(download_video, read_video_urls("data/video_urls.csv"))
        print("parallel results:", results)
        create_report(round(time.perf_counter() - start_time, 2))   