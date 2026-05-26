# Extracts 1000 entries randomly from the master json file

import json
import random

def format_and_extract_subset():
    try:
        with open("master_list.json", "r", encoding="utf-8") as file:
            master_data = json.load(file)

    except Exception as e:
        print(f"An error occured: {e}")
        return

    filteredGames = [
        {
            "appid": game["appid"],
            "name": game["name"]
        }
        for game in master_data
    ]

    sample_size = 2000
    random_subset = random.sample(filteredGames, sample_size)

    try:
        with open("subset_temp.json", "w", encoding="utf-8") as file:
            json.dump(random_subset, file, indent=4)

    except Exception as e:
        print(f"An error occured: {e}")
        return
