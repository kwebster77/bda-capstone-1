from pathlib import Path
import yt_dlp
import csv
import time


def download_video(url):
    Path("videos").mkdir(exist_ok=True)

    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "socket_timeout": 30,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])

        return {
            "url": url,
            "status": "success",
            "error": "",
        }

    except Exception as error:
        return {
            "url": url,
            "status": "failed",
            "error": str(error),
        }


def read_video_urls(csv_path):
    urls = []
    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row["url"])
    return urls


def create_report(sequential_time, parallel_time, video_count):
    Path("reports").mkdir(exist_ok=True)
    speedup = round(sequential_time / parallel_time, 2) if parallel_time > 0 else 0
    improvement = (
        round((sequential_time - parallel_time) / sequential_time * 100, 2)
        if sequential_time > 0
        else 0
    )

    with open("reports/sequential_report.md", "w") as file:
        file.write(
            f"""# Video Download Performance Report

**Videos downloaded:** {video_count}

## Results

| Method | Time (seconds) |
|--------|---------------:|
| Sequential | {sequential_time} |
| Parallel | {parallel_time} |

## Comparison

- **Speedup:** {speedup}x faster
- **Time saved:** {round(sequential_time - parallel_time, 2)} seconds ({improvement}%)

## Complexity

| Method | Time Complexity | Space Complexity |
|--------|:-:|:-:|
| Sequential | O(n) | O(1) |
| Parallel | O(n/p) | O(p) |

With LLM support to format the mkd file better ;)
"""
        )


def create_failure_report(sequential_results, parallel_results):
    Path("reports").mkdir(exist_ok=True)
    failed_sequential = [r for r in sequential_results if r["status"] == "failed"]
    failed_parallel = [r for r in parallel_results if r["status"] == "failed"]
    all_failed = failed_sequential + failed_parallel

    with open("reports/failed_downloads.md", "w") as file:
        file.write("# Failed Downloads Report\n\n")
        file.write(f"**Total failures:** {len(all_failed)}\n\n")

        if failed_sequential:
            file.write("Sequential Failures\n\n")
            for r in failed_sequential:
                file.write(f"- `{r['url']}` — {r['error']}\n")
            file.write("\n")

        if failed_parallel:
            file.write("Parallel Failures\n\n")
            for r in failed_parallel:
                file.write(f"- `{r['url']}` — {r['error']}\n")
            file.write("\n")

        if not all_failed:
            file.write("No failures recorded.\n")


def get_video_metadata(url):
    ydl_options = {
        "quiet": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "view_count": info.get("view_count"),
            "ext": info.get("ext"),
            "url": url,
        }
    except Exception as error:
        print(f"Failed to get metadata for {url}: {error}")
        return None


def save_metadata_csv(metadata_rows, filepath="data/video_metadata.csv"):
    fieldnames = ["title", "duration", "uploader", "view_count", "ext", "url"]
    with open(filepath, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata_rows)


def collect_metadata(urls):
    metadata_rows = []
    for url in urls:
        metadata = get_video_metadata(url)
        if metadata:
            metadata_rows.append(metadata)
    save_metadata_csv(metadata_rows)
    print(f"Saved metadata for {len(metadata_rows)} videos to data/video_metadata.csv")


def download_sequential(urls):
    results = []
    start_time = time.perf_counter()
    for url in urls:
        result = download_video(url)
        results.append(result)
    elapsed = round(time.perf_counter() - start_time, 2)
    return elapsed, results


def download_parallel(urls):
    from multiprocessing import Pool

    with Pool() as pool:
        start_time = time.perf_counter()
        results = pool.map(download_video, urls)
    elapsed = round(time.perf_counter() - start_time, 2)
    return elapsed, list(results)
