import http.client
import json
from flask import json

token = "sk_live_fovP7Cq6R9x9eDKRaMx3PCSU1aQMrnOR"


def return_data(data_query, token):
    conn = http.client.HTTPSConnection("pokeapi.p.sulu.sh")

    headers = {
        'Accept': "application/json",
        'Authorization': f"Bearer {token}"
    }
    conn.request("GET", data_query, headers=headers)
    res = conn.getresponse()

    # Check if the response status is OK (200)
    if res.status != 200:
        print(f"Request failed with status {res.status}: {res.reason}")
        return None  # Return None if the request failed

    data = res.read()
    return data.decode("utf-8")


def sector_type(sector):
    if sector == "services":
        poke_type = "normal"
    elif sector == "manufacturing":
        poke_type = "fighting"
    elif sector == "aviation":
        poke_type = "flying"
    elif sector == "transport":
        poke_type = "ground"
    elif sector == "energy":
        poke_type = "fire"
    elif sector == "health":
        poke_type = "water"
    elif sector == "technology":
        poke_type = "electric"
    else:
        poke_type = "unknown"
    return poke_type


import json

import json


def find_pokemon(poke_type):
    matching_pokemon = {}
    offset = 0

    while len(matching_pokemon) < 6:
        # Fetch data with current offset
        query = f"/api/v2/pokemon/?limit=50&offset={offset}"
        response_data = return_data(query, token)
        data = json.loads(response_data)

        if 'results' not in data:
            break  # Exit if no results are found (in case of API issues)

        # Loop through each Pokémon result in the data
        for pokemon in data['results']:
            poke_url = pokemon['url'][pokemon['url'].find("/api"):]
            poke_details = return_data(poke_url, token)
            poke_info = json.loads(poke_details)

            # Check Pokémon's type
            for poke_type_info in poke_info.get('types', []):
                if poke_type_info['type']['name'] == poke_type:
                    # Extract attack stat
                    attack_stat = next(
                        (stat['base_stat'] for stat in poke_info['stats'] if stat['stat']['name'] == "attack"), None
                    )
                    # Extract dream_world icon URL
                    icon_url = poke_info['sprites']['other']['dream_world'].get('front_default', None)

                    # Add Pokémon's name, id, attack, and icon to the dictionary
                    matching_pokemon[pokemon['name']] = {
                        "id": poke_info['id'],
                        "attack": attack_stat,
                        "icon": icon_url
                    }
                    break  # Stop checking other types for this Pokémon

            # Stop if we’ve collected 6 matching Pokémon
            if len(matching_pokemon) == 6:
                break

        # Update offset to fetch the next batch of Pokémon
        offset += 50

        # Break if we reach the end of available Pokémon (no more results)
        if len(data['results']) == 0:
            break

    return matching_pokemon


def candle_sections(candle_values):
    return 0


print(find_pokemon("water"))
