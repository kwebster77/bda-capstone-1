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

def create_report(sequential_time):
    with open("reports/sequential_report.md", "a") as file:
        # file.write(f"Total time: {sequential_time} seconds")
        # file.write("What is the time complexity and space complexity of downloading the videos one by one?")
        # file.write("Time complexity: O(n)")
        # file.write("Space complexity: O(1)")
        file.write (f"parallel execution: {sequential_time} seconds")
        # file.write (f"Speed improvement: {round((time - parallel_time) / time * 100, 2)}%", "\n")