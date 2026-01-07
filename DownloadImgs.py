import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def downloadImg(url):
    req = requests.get(url, timeout=15)
    req.raise_for_status()
    return req.content


def readSpriteFromPKMNFile(path, outputPath):
    with open(path, "r") as f:
        data = json.load(f)

    links = readLinksFromDict(data["sprites"], outputPath)

    def download_and_write(rel_path, url):
        out_dir = os.path.join("images", os.path.dirname(rel_path))
        os.makedirs(out_dir, exist_ok=True)

        out_file = os.path.join("images", rel_path + ".png")
        with open(out_file, "wb") as f:
            f.write(downloadImg(url))

    # Tune max_workers depending on network / API limits
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [
            executor.submit(download_and_write, path, url)
            for path, url in links.items()
        ]

        for future in as_completed(futures):
            future.result()  # raises if a download failed




def cleanEmptyDir():
    os.system(r"""for /f "delims=" %d in ('dir /s /b /ad ^| sort /r') do rd "%d" """)


def readLinksFromDict(data, base_path):
    links = {}

    for key, value in data.items():
        current_path = os.path.join(base_path, key)

        if isinstance(value, dict):
            links.update(readLinksFromDict(value, current_path))
        elif isinstance(value, str):
            links[current_path] = value

    return links

for file in os.listdir(os.path.join("pokeapi", "pokemon")):
    monname = file.split(".")[0]
    readSpriteFromPKMNFile(
        os.path.join("pokeapi", "pokemon", f"{monname}.json"),
        monname
    )
cleanEmptyDir()