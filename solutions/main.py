from library import (
    read_video_urls,
    collect_metadata,
    download_sequential,
    download_parallel,
    create_report,
    create_failure_report,
)


if __name__ == "__main__":
    urls = read_video_urls("data/video_urls.csv")

    collect_metadata(urls)

    sequential_time, sequential_results = download_sequential(urls)
    print(f"Sequential time: {sequential_time}s")

    parallel_time, parallel_results = download_parallel(urls)
    print(f"Parallel time: {parallel_time}s")

    create_report(sequential_time, parallel_time, len(urls))
    create_failure_report(sequential_results, parallel_results)
