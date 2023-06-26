import ast

# Installed Imports
from flask import Blueprint, request, url_for, jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.dialects.postgresql import insert

# Custom imports
from src import app, utils
from src.models import db
from src.models import Pokemon, PokemonSchema


pokemon_api = Blueprint("pokemon_api", __name__, url_prefix="/api/pokemons")


# Creating custom error handlers
class PokemonException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


class NotFoundError(Exception):
    def __init__(self, message, code=404):
        self.message = message
        self.code = code


class InvalidFormat(Exception):
    def __init__(self, message, code=415):
        self.message = message
        self.code = code


@pokemon_api.errorhandler(NotFoundError)
def not_found_error(e):
    return {
        "error": f"Not Found: {e}",
        "message": "The reuqested query could not be found",
    }, 404


@pokemon_api.errorhandler(PokemonException)
def name_already_exist(e):
    return {
        "error": "Name already exists",
        "message": "Resource already exists in the system",
    }, 405


@pokemon_api.errorhandler(InvalidFormat)
def invalid_name_format(e):
    return {
        "error": "Unsupported Media type",
        "message": "server refuses to accept the request because of the payload format is an unsupported format",
    }, 422


@pokemon_api.errorhandler(SQLAlchemyError)
def handle_sql_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": str(e)}, 400


# <<<<<<<<<<<<<<<<  Pokemon APIs   >>>>>>>>>>>>>>>>>>>>>>>>


@pokemon_api.route("/", methods=["GET"])
@pokemon_api.route("/<pokemon_id>", methods=["GET"])
def get_pokemons(pokemon_id=None):
    """
    This API method returns a list of all available pokemon and
    manual search results to get a list of specific pokemon details.
    """

    search = request.args.get("search")
    search_by_type_1 = request.args.get("search_by_type_1")
    search_by_type_2 = request.args.get("search_by_type_2")
    legendary_search = request.args.get("legendary_search")
    # search_total = request.args.get("search_total")
    generation = request.args.get("generation")
    name_prefix = request.args.get("name_prefix")
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    query = Pokemon.query

    if pokemon_id:
        query = query.filter(Pokemon.id == pokemon_id)
        if not query:
            raise PokemonException(f"{pokemon_id} doesn't exist", 404)

    query = query.order_by(getattr(getattr(Pokemon, sort), order)())

    if search:
        query = query.filter(Pokemon.name.ilike(f"%{search}%"))
    if name_prefix:
        name_prefix = name_prefix.capitalize()
        query = query.filter(Pokemon.name.startswith("name_prefix"))
    if search_by_type_1:
        query = query.filter(Pokemon.type_1.ilike(f"%{search_by_type_1}%"))
    if search_by_type_2:
        query = query.filter(Pokemon.type_2.ilike(f"{search_by_type_2}%"))
    if legendary_search:
        legendary_search = ast.literal_eval(legendary_search)
        query = query.filter(Pokemon.legendary.is_(legendary_search))
    if generation:
        query = query.filter(Pokemon.generation == generation)

    # if search_total:
    #     query = query.filter(Pokemon.attack <= search_total)

    # Paginate the query
    pokemons = query.paginate(page=page, per_page=per_page, error_out=False)

    # serialize the data
    schema = PokemonSchema(many=True)
    serialize_pokemons = schema.dump(pokemons)

    if len(serialize_pokemons) == 0:
        raise NotFoundError(f"No Pokemon found in the list")
    if pokemons.has_next:
        next_page = url_for(
            "pokemon_api.get_pokemons", page=pokemons.next_num, _external=True
        )
    else:
        next_page = None

    return {
        "total": pokemons.total,
        "page": pokemons.page,
        "per_page": per_page,
        "pokemons": serialize_pokemons,
        "next_page": next_page,
    }, 200


@pokemon_api.route("/", methods=["POST"])
def create_pokemons():
    """
    This API allows to create new pokemon, using the given attributes.
    """
    pokemon_data = request.json
    if isinstance(pokemon_data, dict):
        pokemon_data = [pokemon_data]  # Convert to a list for consistency

    # Track the number of successfully added Pokemon
    success_count = 0

    for item in pokemon_data:
        rank = item.get("rank")
        name = item.get("name")
        type_1 = item.get("type_1")
        type_2 = item.get("type_2")
        total = item.get("total")
        hp = item.get("hp")
        attack = item.get("attack")
        defense = item.get("defense")
        sp_atk = item.get("sp_atk")
        sp_def = item.get("sp_def")
        speed = item.get("speed")
        generation = item.get("generation")
        legendary = item.get("legendary")

        existing_pokemon = Pokemon.query.filter_by(name=name).first()
        if existing_pokemon:
            raise PokemonException(
                f"Pokemon with name {existing_pokemon.name} already exists"
            )
        if not name.isalpha():
            raise InvalidFormat

        try:
            pokemon = Pokemon(
                rank=rank,
                name=name,
                type_1=type_1,
                type_2=type_2,
                total=total,
                hp=hp,
                attack=attack,
                defense=defense,
                sp_atk=sp_atk,
                sp_def=sp_def,
                speed=speed,
                generation=generation,
                legendary=legendary,
            )
            db.session.add(pokemon)

            # to include the count in the response message
            success_count += 1
        except (SQLAlchemyError, IntegrityError) as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}, 500

    db.session.commit()

    return {
        "success": True,
        "message": f"{success_count} Pokemon added successfully",
    }


@pokemon_api.route("/", methods=["PUT", "POST"])
def update_pokemons():
    """
    This API method updates the pokemon(s), using the JSON format.
    We can pass the values in the body to be updates partially/fully.
    """

    pokemon_data = request.json.get("pokemon")
    upsert_pokemons = []
    if not pokemon_data:
        raise NotFoundError

    try:
        for items in pokemon_data:
            existing_pokemon = Pokemon.query.filter_by(name=items.get("name")).first()
            if existing_pokemon:
                for column in Pokemon.__table__.columns:
                    column_name = column.name
                    if column_name not in ["id", "name", "type_1"]:
                        items[column_name] = items.get(
                            column_name, getattr(existing_pokemon, column_name)
                        )
                    else:
                        items[column_name] = items.get(
                            column_name, getattr(existing_pokemon, column_name)
                        )

                    upsert_pokemons.append(items)

            # Below dictionary will update from the payload
            stmt = insert(Pokemon).values(pokemon_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=[Pokemon.name],  # change to name from id
                set_={
                    "rank": stmt.excluded.rank,
                    "name": stmt.excluded.name,
                    "type_1": stmt.excluded.type_1,
                    "type_2": stmt.excluded.type_2,
                    "total": stmt.excluded.total,
                    "hp": stmt.excluded.hp,
                    "attack": stmt.excluded.attack,
                    "defense": stmt.excluded.defense,
                    "sp_atk": stmt.excluded.sp_atk,
                    "sp_def": stmt.excluded.sp_def,
                    "speed": stmt.excluded.speed,
                    "generation": stmt.excluded.generation,
                    "legendary": stmt.excluded.legendary,
                },
            )

            db.session.execute(stmt)
            db.session.commit()
            return {"success": True, "message": "Pokemon updated successfully"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        raise PokemonException


@pokemon_api.route("/", methods=["DELETE"])
@pokemon_api.route("/<pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id=None):
    """
    This API method is used to delete the specified Pokemon(s) by
    passing multiple ID(s) in the JSON body.
    """
    try:
        # Here, taking the ids in the JSON format
        pokemon_data = request.json.get("pokemon")
        if not pokemon_data:
            raise NotFoundError(f"No pokemon data found for deletion", 404)

        for item in pokemon_data:
            item_id = item.get("id")
            if not item_id:
                raise NotFoundError("No Id provided for deletion", 404)

            pokemon = Pokemon.query.filter_by(id=item_id).first()
            if not pokemon:
                raise NotFoundError(f"No pokemon id: {item_id} found", 404)

            db.session.delete(pokemon)
        db.session.commit()
        return {
            "status": True,
            "message": f"Pokemon id deleted successfully",
        }, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        raise PokemonException
