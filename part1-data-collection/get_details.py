import requests
import json
import time

def is_explicit(game_data):
    descriptors = game_data.get("content_descriptors", {})
    ids = descriptors.get("ids", [])

    explicit_ids = {1, 3}

    if any(id in ids for id in explicit_ids):
        return True
    return False

def filter_explicit():
    try:
        with open("details_temp.json", "r", encoding="utf-8") as file:
            details = json.load(file)
    
    except Exception as e:
        print(f"An error occured: {e}")

    filtered_list = []

    for game_data in details:
        if not is_explicit(game_data):
            filtered_list.append(game_data)
    
    try:
        with open("filtered_list.json", "w", encoding="utf-8") as file:
            json.dump(filtered_list, file, indent=4)
        
    except Exception as e:
        print(f"An error occured: {e}")

def fetch_game_data(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&filters=basic,price_overview,genres,release_date,content_descriptors"

    try:
        response = requests.get(url)

        # Check for successful call
        if response.status_code == 200:
            # Convert bulk data to json
            json_data = response.json()

            if json_data and json_data[str(appid)]["success"]:
                game_data = json_data[str(appid)]["data"]
                return game_data
            else:
                print(f"AppID {appid} found, but api 'success' flag was false.")
                return "SKIP"
            
        elif response.status_code == 429:
            return "RATE_LIMITED"

        else:
            print(f"Failed to fetch data, status code: {response.status_code}")

    except Exception as e:
        print(f"An error occured: {e}")
        return

def get_and_filter_app_details():
    try:
        with open("subset_temp.json", "r", encoding="utf-8") as file:
            subset_data = json.load(file)
        
    except Exception as e:
        print(f"An error occured: {e}")
        return

    game_json = []

    for game in subset_data:
        success = False
        while not success:
            game_data = fetch_game_data(game["appid"])

            if game_data == "SKIP":
                print("Skipping a deleted game.")
                success = True

            elif game_data == "RATE_LIMITED":
                print("Rate limited, trying again.")
                time.sleep(10)
            
            elif game_data:
                game_json.append(game_data)
                success = True
                time.sleep(1.5)
                  
    try:
        with open("details_temp.json", "w", encoding="utf-8") as file:
            json.dump(game_json, file, indent=4)
    except Exception as e:
        print(f"An error occured: {e}")

get_and_filter_app_details()
filter_explicit()
