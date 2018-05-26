import json
import sys
import util
import os
import config

whitelist = {   
    ##### Meats etc. #####
    124120: "Leyblood",
    124117: "Lean Shank",
    124121: "Wildfowl Egg",
    142336: "Falcosaur Egg",
    124118: "Fatty Bearsteak",
    124119: "Big Gamy Ribs",
    133680: "Slice of Bacon",

    ##### Fishing #####
    124112: "Black Barracuda",
    124110: "Stormray",
    124111: "Runescale Koi",
    124109: "Highmountain Salmon",
    133607: "Silver Mackerel",
    124107: "Cursed Queenfish",
    124108: "Mossgill Perch",

    ##### Cooking #####
    133579: "Lavish Suramar Feast",

    # Cooking Rank 3
    133571: "Azshari Salad",
    133574: "Fishbrul Special",
    133572: "Nightborne Delicacy Platter",
    133573: "Seed-Battered Fish Plate",
    33570: 	"The Hungry Magister",

    # Cooking Rank 2
    133567: "Barracuda Mrglgagh",
    133569: "Drogbar-Style Salmon",
    133568: "Koi-Scented Stormray",
    133565: "Leybeque Ribs",
    133566: "Suramar Surf and Turf",

    ##### Herbalism #####
    124102: "Dreamleaf",
    124103: "Foxflower",
    124105: "Starlight rose",
    124101: "Aethril",
    124104: "Fjarnskaggl",
    128304: "Yseralline Seed",
    124106: "Felwort",
    151565: "Astral Glory",

    ##### Alchemy #####
    # Flasks
    127850: "Flask of Ten Thousand Scars",
    127849: "Flask of the Countless Armies",
    127848: "Flask of the Seventh Demon",
    127847: "Flask of the Whispered Pact",

    # Potions
    127846: "Leytorrent Potion",
    127843: "Potion of Deadly Grace",
    142117: "Potion of Prolonged Power",
    127844: "Potion of the Old War",
    127845: "Unbending Potion",
    127835: "Ancient Mana Potion",

    # Trinkets
    127842: "Infernal Alchemist Stone",

    # Utility Potions
    127840: "Skaggldrynk",

    ##### Skinning #####
    151566: "Fiendish Leather",

    ##### Tailoring #####
    151567: "Lightweave Cloth",

    ##### Miscellaneous #####
    124125: "Obliterum",
    152296: "Primal Obliterum",

    ##### Enchanting #####
    124442: "Chaos Crystal",
    124441: "Leylight Shard",
    124440: "Arkhana",

    # Enchants
    128541: "Enchant Ring - Binding of Critical Strike",
    128542: "Enchant Ring - Binding of Haste",
    128543: "Enchant Ring - Binding of Mastery",
    128544: "Enchant Ring - Binding of Versatility",
    128537: "Enchant Ring - Word of Critical Strike",
    128538: "Enchant Ring - Word of Haste",
    128539: "Enchant Ring - Word of Mastery",
    128540: "Enchant Ring - Word of Versatility",

    128549: "Enchant Cloak - Binding of Agility",
    128550: "Enchant Cloak - Binding of Intellect",
    128548: "Enchant Cloak - Binding of Strength",
    128546: "Enchant Cloak - Word of Agility",
    128547: "Enchant Cloak - Word of Intellect",
    128545: "Enchant Cloak - Word of Strength",

    141910: "Enchant Neck - Mark of the Ancient Priestess",
    128551: "Enchant Neck - Mark of the Claw",
    128552: "Enchant Neck - Mark of the Distant Army",
    141908: "Enchant Neck - Mark of the Heavy Hide",
    128553: "Enchant Neck - Mark of the Hidden Satyr",
    141909: "Enchant Neck - Mark of the Trained Soldier",
    144307: "Enchant Neck - Mark of the Deadly",
    144304: "Enchant Neck - Mark of the Master",
    144306: "Enchant Neck - Mark of the Quick",
    144305: "Enchant Neck - Mark of the Versatile",

    128558: "Enchant Gloves - Legion Herbalism",
    128559: "Enchant Gloves - Legion Mining",
    128560: "Enchant Gloves - Legion Skinning",
    128561: "Enchant Gloves - Legion Surveying",

    128554: "Enchant Shoulder - Boon of the Scavenger",

    ##### Mining #####
    124444: "Infernal Brimstone",
    151564: "Empyrium",
    123919: "Felslate",
    123918: "Leystone Ore",

    ##### Jewelcrafting #####
    151718: "Argulite",
    151720: "Chemirine",
    151722: "Florid Malachite",
    151721: "Hesselian",
    151579: "Labradorite",
    151719: "Lightsphene",
    129100: "Gem Chip",

    151580: "Deadly Deep Chemirine",
    151584: "Masterful Argulite",
    151583: "Quick Lightsphene",
    151585: "Versatile Labradorite",

    151587: "Empyrial Cosmic Crown",
    151588: "Empyrial Deep Crown",
    151589: "Empyrial Elemental Crown",
    151590: "Empyrial Titan Crown",

    127842: "Infernal Alchemist Stone",

    138793: "Tome of Illusions: Pandaria",
	138791: "Tome of Illusions: Cataclysm",
	138790: "Tome of Illusions: Northrend",
	138789: "Tome of Illusions: Outland",
	138787: "Tome of Illusions: Azeroth",

	### Old materials ###
	74248: "Sha Crystal",
	76141: "Imperial Amethyst",
	76139: "Wild Jade",
	76140: "Vermilion Onyx",

	52722: "Maelstrom Crystal",
	52721: "Heavenly Shard",
	52328: "Volatile Air",
	52327: "Volatile Earth",

	34057: "Abyss Crystal",
	34052: "Dream Shard",
	34055: "Greater Cosmic Essence",
	35622: "Eternal Water",

	22450: "Void Crystal",
	22449: "Large Prismatic Shard",
	21884: "Primal Fire",
	22457: "Primal Mana",

	14344: "Large Brilliant Shard",
	7078:  "Essence of Fire",
	7080:  "Essence of Water",
	12808: "Essence of Undeath",
    
    ##### Inscription #####

    # Materials
    39469: "Moonglow Ink",
    39774: "Midnight Ink",

    # Legion Materials
    129034: "Sallow Pigment",
    129032: "Roseate Pigment",
    39151:  "Alabaster Pigment",

    # Legion Recipes
    151610: "Vantus Rune: Antorus, the Burning Throne",
    141446: "Tome of the Tranquil Mind",
    141333: "Codex of the Tranquil Mind",

    # Glyphs
    43551:  "Glyph of Foul Menagerie",
    104099: "Glyph of the Skeleton",
    129029: "Glyph of Crackling Flames",
    139417: "Glyph of Fallow Wings",
    129028: "Glyph of Fel Touched Souls",
    139435: "Glyph of Fel Wings",
    139436: "Glyph of Tattered Wings",
    44922:  "Glyph of Stars",
    137249: "Glyph of Arachnophobia",
    137239: "Glyph of the Hook",
    137261: "Glyph of the Skullseye",
    139338: "Glyph of Crackling Crane Lightning",
    43366:  "Glyph of Winged Vengeance",
    104127: "Glyph of Lingering Ancestors",
    151538: "Glyph of Ember Shards",
    139310: "Glyph of the Shivarra",
}

def download_and_filter_auction_data(realm=None):
    
    auctions = util.download_auctions_json(realm) if realm is not None else util.download_auctions_json();
    print("Auctions before: ", len(auctions))
    auctions = [x for x in auctions if x['item'] in whitelist]
    print("Auctions after: ", len(auctions))
    
    # Save filtered auctions
    with open(os.path.join(config.SAVE_DIR_JSON_FILTERED, config.SAVE_NAME_FILTERED), 'w') as outfile:
        json.dump(auctions, outfile)

if __name__ == "__main__":
    download_and_filter_auction_data()