import urllib.request
import json
import pprint
import sys
import os
import glob
import datetime
import config

AUCTIONS_URL_BASE = "https://eu.api.battle.net/wow/auction/data/{realm}?locale={locale}&apikey={api_key}"
ITEMS_URL_BASE = "https://us.api.battle.net/wow/item/{item}?locale={locale}&apikey={api_key}"

def download_auctions_json(realm=config.DEFAULT_REALM):
    url_paramterized = AUCTIONS_URL_BASE.replace("{realm}", realm).replace("{locale}", config.LOCALE_AUCTION).replace("{api_key}", config.API_KEY)
    url_data = None

    try:
        with urllib.request.urlopen(url_paramterized) as url:
            data = json.loads(url.read().decode())

            url_data = data["files"][0]["url"]
            lastModified = data["files"][0]["lastModified"]

            print("Last auctions update:", datetime.datetime.fromtimestamp(lastModified/1000.0))

            cached = check_for_cached_auctions(lastModified)
            if cached is not None:
                print("Found cached download, let's not download it again..")
                return cached
            else:
                if url_data is None:
                    print("Error! No URL could be found at the given address: ", url_paramterized)
                    return

                with urllib.request.urlopen(url_data) as url:
                    data = json.loads(url.read().decode())

                    with open(os.path.join(config.SAVE_DIR_JSON, str(lastModified) + ".json"), 'w') as outfile:
                        json.dump(data["auctions"], outfile)
                    
                    print("Downloaded auctions for:", data["realms"][0]["name"])

                    return data["auctions"]

            return auctions
    except urllib.error.HTTPError as err:
        raise Exception("Error! Invalid URL: " + url_paramterized)

def check_for_cached_auctions(lastModified):
    path = os.path.join(config.SAVE_DIR_JSON, str(lastModified) + ".json")

    for file in glob.glob(os.path.join(config.SAVE_DIR_JSON, "*.json")):
        if file == path:
            with open(path) as f:
                data = json.load(f)
                return data
        else:
            os.remove(file) # delete old json files

    return None