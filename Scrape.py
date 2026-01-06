import requests
import json

def fetchAllLinks(url):
    count = requests.get(url)
    count.raise_for_status()
    count = count.json()["count"]
    full = requests.get(url+"?offset=0&limit="+str(count))
    full.raise_for_status()
    full = full.json()
    out = {}
    for item in full["results"]:
        if "name" not in item.keys():
            out[full["results"].index(item)] = item["url"]
        else:
            out[item["name"]] = item["url"]
    return out


topLev = requests.get('https://pokeapi.co/api/v2/')
topLev.raise_for_status()
topLev = list(topLev.json().values())
alllinks = {}
for i in range(len(topLev)):
    print(topLev[i])
    alllinks[topLev[i]] = fetchAllLinks(topLev[i])


json.dump(alllinks, open("alllinks.json", "w"),indent=2)