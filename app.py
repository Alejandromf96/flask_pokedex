from flask import Flask, render_template, request
import requests

app = Flask(__name__)

POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"
POKE_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"

@app.route('/', methods=['GET', 'POST'])
def index():
    pokemon = None
    error = None

    if request.method == 'POST':
        search = request.form.get("search", "").lower().strip()
        if search:
            response = requests.get(f"{POKE_API_URL}{search}")
            if response.status_code == 200:
                pokemon_data = response.json()

                species_response = requests.get(f"{POKE_SPECIES_URL}{search}")
                description = None
                if species_response.status_code == 200:
                    species_data = species_response.json()
                    for entry in species_data["flavor_text_entries"]:
                        if entry["language"]["name"] == "en":
                            description = entry["flavor_text"].replace("\n", "").replace("\f", " ")
                            break
                        if not description:
                            description = "There's no description available"

                pokemon = {
                    "name": pokemon_data["name"].capitalize(),
                    "image": pokemon_data["sprites"]["front_default"],
                    "types": [t["type"]["name"].capitalize() for t in pokemon_data["types"]],
                    "description": description,
                    "stats": {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]},
                }
            else:
                error = f"No Pokemon named '{search}'."

    return render_template("index.html", pokemon=pokemon, error=error)

if __name__ == "__main__":
    app.run(debug=True)