import http.client
import json
from flask import json
from pprint import pprint


token = "sk_live_fovP7Cq6R9x9eDKRaMx3PCSU1aQMrnOR"
types = ["normal", "fighting", "rock", "ground", "fire", "water", "electric"]
type_sector = {"normal":"services",
               "fighting":"manufacturing",
               "rock":"raw materials",
               "ground":"transport",
               "fire":"energy",
               "water":"health",
               "electric":"technology"}


def return_data(data_query, api_key):
    conn = http.client.HTTPSConnection("pokeapi.p.sulu.sh")

    headers = {
        'Accept': "application/json",
        'Authorization': f"Bearer {api_key}"
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
    elif sector == "raw materials":
        poke_type = "rock"
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
                    matching_pokemon[str(poke_type)+"_"+str(len(matching_pokemon))] = {
                        "name": pokemon['name'],
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


def all_pokemon():
    total_pokemon = {"result": {}}
    for pokemon_type in types:  # Loop over the defined types
        matching_pokemon = find_pokemon(pokemon_type)  # Assuming find_pokemon function exists
        # Store the matching Pokémon under the current type in the result dictionary
        total_pokemon["result"][pokemon_type] = matching_pokemon

    return total_pokemon


def rank_pokemon(data):
    ranked_data = {}

    for p_type, p_list in data['result'].items():
        # Sort Pokémon in each type by attack power in descending order
        sorted_pokemon = sorted(p_list.items(), key=lambda x: x[1]['attack'], reverse=True)

        # Assign rank based on sorted position
        ranked_data[p_type] = {
            f"{name}_ranked": {**pokemon, "rank": rank}
            for rank, (name, pokemon) in enumerate(sorted_pokemon)
        }

    return ranked_data



pprint(rank_pokemon(all_pokemon()))

