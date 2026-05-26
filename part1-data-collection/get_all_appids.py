# This script fetches the master list of appIDs from the steam
# store in theory. In practice, the api is down so i downloaded
# a list of appids that i then worked with. 
# Credits to jsnli on github for the json file.

import requests
import json
import time

def fetch_game_ids():
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    try:
        response = requests.get(url, timeout=30)

        # Check for successful call
        if response.status_code == 200:
            # Convert bulk data to json
            json_data = response.json()

            with open("master_list.json", "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4)
            
            print("Successfully created bulk list to 'master_list.json'!")

        else:
            print(f"Failed to fetch data, status code: {response.status_code}")
    except Exception as e:
        print(f"An error occured: {e}")
        return

fetch_game_ids()
