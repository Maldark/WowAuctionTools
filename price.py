import urllib.request
import json
import pprint
import sys
import util
import config

DEFAULT_REALM = "Stormscale"

def find_prices(item_ids):
    if not isinstance(item_ids, list):
        item_ids = [item_ids]

    ret = []
    
    auctions = util.download_auctions_json()

    for index, item_id in enumerate(item_ids):
        item_id_int = int(item_id)

        items_url_paramterized = util.ITEMS_URL_BASE.replace("{locale}", config.LOCALE_ITEM).replace("{api_key}", config.API_KEY).replace("{item}", item_id)
        item_name = None

        try:
            with urllib.request.urlopen(items_url_paramterized) as url:
                data = json.loads(url.read().decode())
                item_name = data["name"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("Error! No such item could be found!")
                return
    
        lowest_price = min([x['buyout'] for x in auctions if x['item'] == item_id_int])
        lowest_price_str = str(lowest_price)
        print("{} sells for {}g {}s {}c".format(item_name, lowest_price_str[:-4], lowest_price_str[-4:-2], lowest_price_str[-2:]))

        ret.insert(len(ret), lowest_price)

    return ret

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Error: No item specified")
        sys.exit(0)
    else:
        items = sys.argv[1:]
        prices = find_prices(items)
        print(prices)
