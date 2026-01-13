import requests
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

count = 0
count_lock = threading.Lock()
total = 0


def getJSON(key: str, url: str):
    global count

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    with count_lock:
        count += 1
        print(f"{count}/{total}", end="\r")

    return key, response.json()


def readAllLinksAndPullJsons(TLF: str):
    jsons = {}

    with open("alllinks.json", "r") as f:
        urllist = json.load(f)["https://pokeapi.co/api/v2/" + TLF + "/"]

    # Tune max_workers as needed (8–16 is reasonable)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(getJSON, key, url)
            for key, url in urllist.items()
        ]

        for future in as_completed(futures):
            key, data = future.result()
            jsons[key] = data

    outputJSON(jsons, TLF)


def countit():
    with open("alllinks.json", "r") as f:
        file = json.load(f)
        c = 0
        for key in file:
            for _ in file[key]:
                c += 1
        return c


def outputJSON(jsons: dict, TLF: str):
    topFolder = os.path.join("pokeapi", TLF)
    os.makedirs(topFolder, exist_ok=True)

    for name, data in jsons.items():
        with open(os.path.join(topFolder, name + ".json"), "w") as f:
            json.dump(data, f, indent=2)


total = countit()
with open("alllinks.json", "r") as f:
    file = json.load(f)
    for key in file:
        print(os.path.split(key)[0].split("/")[-1])
        readAllLinksAndPullJsons(os.path.split(key)[0].split("/")[-1])
