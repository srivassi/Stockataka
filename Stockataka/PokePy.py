import http.client
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


def find_pokemon(poke_type):
    matching_pokemon = {}
    query = "/api/v2/pokemon/?limit=100&offset=0"
    response_data = return_data(query, token)
    data = json.loads(response_data)
    # Loop through each Pokémon result in the data
    for pokemon in data.get('results', []):
        poke_url = pokemon['url'][pokemon['url'].find("/api"):]
        poke_details = return_data(poke_url, token)
        poke_info = json.loads(poke_details)
        # Check Pokémon's type
        for poke_type_info in poke_info.get('types', []):
            if poke_type_info['type']['name'] == poke_type:
                matching_pokemon[pokemon['name']]= poke_info['id']
                break

    return matching_pokemon

print(find_pokemon("electric"))