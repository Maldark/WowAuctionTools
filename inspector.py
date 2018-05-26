import urllib.request
import json
import pprint
import sys
import util
import config

def inspect(target, realm):    
    target = target[0].capitalize() + target[1:]

    auctions, timestamp = util.download_auctions_json(realm)

    owner_dict = [x for x in auctions if x["owner"] == target]

    unique = []
    unique_names = []
    owner_auctions = {}
    
    items_url_paramterized = util.ITEMS_URL_BASE.replace("{locale}", config.LOCALE_ITEM).replace("{api_key}", config.API_KEY)

    for k,v in enumerate(owner_dict):
        if v["item"] not in unique:
            items_url_final = items_url_paramterized.replace("{item}", str(v["item"]))
            item_name = None

            with urllib.request.urlopen(items_url_final) as url_item:
                data_item = json.loads(url_item.read().decode())
                item_name = data_item["name"]

            if item_name is None:
                print("Error! No item name could be found for item id: ", v["item"])
                return
            
            unique.insert(len(unique), v["item"])
            unique_names.insert(len(unique), item_name)
            owner_auctions[v["item"]] = v

    # owner_auctions_json = json.dumps(owner_auctions)

    print("{} has auctions up for the following items:".format(target))

    # print(owner_auctions_json)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(unique_names)


if __name__ == "__main__":
    user = None
    realm = None
    
    if len(sys.argv) <= 1:
        print("No user specified, assuming {}".format(config.DEFAULT_USER))
        user = config.DEFAULT_USER
    else:
        user = sys.argv[1]
    
    if len(sys.argv) <= 2:
        print("No realm specified, assuming {}".format(config.DEFAULT_REALM))
        realm = config.DEFAULT_REALM
    else:
        realm ="%20".join(sys.argv[2:])

    inspect(user, realm)