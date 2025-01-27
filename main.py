from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# The new pokemon_grid with all 42 Pokémon
pokemon_grid = [
    ["Normal", "Pidgey", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/16.svg', "Rattata", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/19.svg', "Pidgeotto", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/17.svg', "Spearow", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/21.svg', "Pidgeot", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/18.svg', "Raticate", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/20.svg'],
    ["Fighting", "Mankey", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/56.svg', "Primeape", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/57.svg', "Machop", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/66.svg', "Machoke", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/67.svg', "Machamp", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/68.svg', "Hitmonlee", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/106.svg'],
    ["Rock", "Omanyte", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/138.svg', "Onix", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/95.svg', "Omastar", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/139.svg', "Geodude", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/74.svg', "Graveler", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/75.svg', "Golem", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/76.svg'],
    ["Ground", "Cubone", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/104.svg', "Diglett", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/50.svg', "Sandshrew", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/27.svg', "Marowak", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/105.svg', "Sandslash", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/28.svg', "Dugtrio", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/51.svg'],
    ["Fire", "Vulpix", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/37.svg', "Charmander", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/4.svg', "Growlithe", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/58.svg', "Ninetales", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/38.svg', "Charmeleon", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/5.svg', "Charizard", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/6.svg'],
    ["Water", "Squirtle", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/7.svg', "Poliwag", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/60.svg', "Psyduck", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/54.svg', "Wartortle", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/8.svg', "Golduck", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/55.svg', "Blastoise", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/9.svg'],
    ["Electric", "Voltorb", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/100.svg', "Magnemite", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/81.svg', "Pikachu", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/25.svg', "Electrode", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/101.svg', "Magneton", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/82.svg', "Raichu", 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/26.svg']
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'selected_pokemon' not in session:
        session['selected_pokemon'] = []

    if request.method == 'POST':
        # Handle any form submission if necessary
        pass

    return render_template('home.html', pokemon_grid=pokemon_grid, selected_pokemon=session['selected_pokemon'])

@app.route('/select_pokemon/<int:row>/<int:col>')
def select_pokemon(row, col):
    selected_pokemon = session.get('selected_pokemon', [])
    position = (row, col)

    if position in selected_pokemon:
        selected_pokemon.remove(position)  # Deselect Pokémon
    else:
        if len(selected_pokemon) < 6:
            selected_pokemon.append(position)  # Select Pokémon

    session['selected_pokemon'] = selected_pokemon
    return redirect(url_for('home'))


@app.route('/submit_team')
def submit_team():
    selected_pokemon = session.get('selected_pokemon', [])
    team_pokemon = []

    # Loop through selected positions and fetch Pokémon data
    for position in selected_pokemon:
        row, col = position
        name = pokemon_grid[row][col]  # Get the Pokémon name
        image_url = pokemon_grid[row][col + 1]  # Get the image URL (this is the next element in each row)
        team_pokemon.append((row, col, name, image_url))

    return render_template('submit_team.html', selected_pokemon=team_pokemon, pokemon_grid=pokemon_grid)


@app.route('/reset')
def reset():
    session['selected_pokemon'] = []
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
