from pathlib import Path
import yt_dlp
import csv
import time


def download_video(url):
    Path("videos").mkdir(exist_ok=True)

    # Save inside videos/ using the video title as the filename
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download([url])

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
    improvement = round((sequential_time - parallel_time) / sequential_time * 100, 2) if sequential_time > 0 else 0

    with open("reports/sequential_report.md", "w") as file:
        file.write("# Video Download Performance Report\n\n")
        file.write(f"**Videos downloaded:** {video_count}\n\n")
        file.write("## Results\n\n")
        file.write("| Method | Time (seconds) |\n")
        file.write("|--------|---------------:|\n")
        file.write(f"| Sequential | {sequential_time} |\n")
        file.write(f"| Parallel | {parallel_time} |\n\n")
        file.write("## Comparison\n\n")
        file.write(f"- **Speedup:** {speedup}x faster\n")
        file.write(f"- **Time saved:** {round(sequential_time - parallel_time, 2)} seconds ({improvement}%)\n\n")
        file.write("## Complexity\n\n")
        file.write("| Method | Time Complexity | Space Complexity |\n")
        file.write("|--------|:-:|:-:|\n")
        file.write("| Sequential | O(n) | O(1) |\n")
        file.write("| Parallel | O(n/p) | O(p) |\n\n")
        file.write("With LLM Support to format the mkd file ;)")

def get_video_metadata(url):
    ydl_options = {
        "quiet": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)
    metadata = {
        "title": info.get("title"),
        "duration": info.get("duration"),
        "uploader": info.get("uploader"),
        "view_count": info.get("view_count"),
        "ext": info.get("ext"),
        "url": url,
    }
    return metadata

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
        metadata_rows.append(metadata)
    save_metadata_csv(metadata_rows)
    print(f"Saved metadata for {len(metadata_rows)} videos to data/video_metadata.csv")

def download_sequential(urls):
    start_time = time.perf_counter()
    for url in urls:
        download_video(url)
    return round(time.perf_counter() - start_time, 2)

def download_parallel(urls):
    from multiprocessing import Pool
    with Pool() as pool:
        start_time = time.perf_counter()
        pool.map(download_video, urls)
    return round(time.perf_counter() - start_time, 2)