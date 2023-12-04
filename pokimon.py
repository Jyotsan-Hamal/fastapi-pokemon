import requests

def fetch_pokemon_data():
    
    url = "https://pokeapi.co/api/v2/pokemon"
    offset = 500
    limit =300
    new_url = f"{url}?offset={offset}&limit={limit}"
    response = requests.get(new_url)
    data = response.json()

    pokemons = []
    
 
    
    for pokemon in data['results']:
        pokemon_data = requests.get(pokemon['url']).json()
        
        name = pokemon_data['name']
        # print(f"Pokimon name : {name}")
        image = pokemon_data['sprites']['front_default']
        # print(f"Pokimon image : {image}")
        types = [type['type']['name'] for type in pokemon_data['types']]
        
        pokemons.append({
            'name': name,
            'image': image,
            'types': types
        })
        print("done")
        
    return pokemons


def main():
    pokemons = fetch_pokemon_data()

    for pokemon in pokemons:
        print(pokemon)


if __name__=="__main__":
    main()