import json
import time
import sys
import requests

def filter_zero():

    try:
        with open("final_scraped_data.json", "r", encoding="utf-8") as file:
            updated_apps = json.load(file)
    
    except Exception as e:
        print(f"An error occured: {e}")

    final_list = []

    skipped_count = 0
    max_skips = len(updated_apps) - 800

    for app in updated_apps:

        if skipped_count < max_skips and app["current_players"] == 0:
            skipped_count += 1
            continue

        final_app_dict = {}
        keyword_list = ["name", "required_age", "is_free"]

        for keyword in keyword_list:
            final_app_dict[keyword] = app[keyword]
        
        price_data = app.get("price_overview")

        if price_data:
            final_app_dict["initial_price"] = price_data.get("initial", 0)
            final_app_dict["discount_percent"] = price_data.get("discount_percent", 0)
        else:
            final_app_dict["initial_price"] = 0
            final_app_dict["discount_percent"] = 0

        genre_list = ["Action", "Adventure", "RPG", "Indie", "Strategy"]

        final_app_dict["isOther"] = 0

        actual_genre_list = app.get("genres")
        if actual_genre_list:
            actual_genres = [d["description"] for d in actual_genre_list]

            for genre in genre_list:
                if genre in actual_genres:
                    final_app_dict["is" + genre] = 1
                else:
                    final_app_dict["is" + genre] = 0

            if any(d.get("description") not in genre_list for d in actual_genre_list):
                final_app_dict["isOther"] = 1
        else:
            final_app_dict["isOther"] = 1
            final_app_dict["isAction"] = 0
            final_app_dict["isAdventure"] = 0
            final_app_dict["isRPG"] = 0
            final_app_dict["isIndie"] = 0
            final_app_dict["isStrategy"] = 0
        
        if not app["release_date"]["coming_soon"]:
            final_app_dict["release_year"] = app["release_date"]["date"][-4:]
        else:
            final_app_dict["release_year"] = 2027
        
        final_app_dict["current_players"] = app["current_players"]
        final_list.append(final_app_dict)

    try:
        with open("final_filtered_data.json", "w", encoding="utf-8") as file:
            json.dump(final_list, file, indent=4)
    
    except Exception as e:
        print(f"An error occured: {e}")


def append_player_count():
    INPUT_FILE = "filtered_list.json"
    OUTPUT_FILE = "final_scraped_data.json"

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            apps_list = json.load(file)
        print(f"Loaded {len(apps_list)} games from {INPUT_FILE}.")
    except Exception as e:
        print(f"An error occured: {e}")

    updated_apps = []

    for app in enumerate(apps_list):
        appid = app.get("steam_appid")
        name = app.get("name")
        
        if not appid:
            continue
            
        url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
        player_count = 0 # Default fallback
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                player_count = data.get("response", {}).get("player_count", 0)
                print(f"Active Players: {player_count}")
            else:
                print(f"Server returned code: {response.status_code}. Defaulting to 0.")
                
        except Exception as e:
            print(f"An error occured: {e}. Defaulting to 0.")
        
        app["current_players"] = player_count
        updated_apps.append(app)
        
        # Save progress line by line
        with open("scraped_backup.jsonl", "a", encoding="utf-8") as backup_file:
            backup_file.write(json.dumps(app) + "\n")
            
        time.sleep(1.5)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(updated_apps, file, indent=4)

filter_zero()