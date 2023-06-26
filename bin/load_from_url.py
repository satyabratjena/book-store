# Below are in-build imports
import requests

# Below are custom imports
from src.models import app, db
from src.models import Pokemon
from src.views import pokemon_api

# <<<<<<< JSON LOAD >>>>>>>>>>>>


# Below is the api for laoding data from url
@pokemon_api.route("/load-pokemons-data")
def load_pokemon():
    load_pokemon_data()
    return "Pokemon data loaded successfully"


def load_pokemon_data():
    with app.app_context():
        # Parsing the JSON data and creating model instances
        url = "https://coralvanda.github.io/pokemon_data.json"
        response = requests.get(url)
        json_data = response.json()
        # Parse the JSON data and map it to your database model
        for item in json_data:
            present_pokemon = Pokemon.query.filter_by(name=item.get("name")).first()

            if present_pokemon:
                return {"error": "Pokemons already present"}

            pokemon = Pokemon(
                rank=item.get("#"),
                name=item.get("Name"),
                type_1=item.get("Type 1"),
                type_2=item.get("Type 2"),
                total=item.get("Total"),
                hp=item.get("HP"),
                attack=item.get("Attack"),
                defense=item.get("Defense"),
                sp_atk=item.get("Sp. Atk"),
                sp_def=item.get("Sp. Def"),
                speed=item.get("Speed"),
                generation=item.get("Generation"),
                legendary=item.get("Legendary"),
            )
            db.session.add(pokemon)
        db.session.commit()


load_pokemon_data()
