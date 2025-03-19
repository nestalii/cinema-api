from flask import jsonify, make_response
from flask import Flask, request

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    # Отримання id з URL параметрів або тіла запиту
    movie_id = request.args.get('id') or get_request_data().get('id')

    if not movie_id:
        return make_response(jsonify({"error": "ID should be specified"}), 400)

    try:
        movie_id = int(movie_id)
    except ValueError:
        return make_response(jsonify({"error": "ID must be an integer"}), 400)

    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return make_response(jsonify({"error": "Record with such id does not exist"}), 400)

    mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(mov), 200)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    if not all(value for key, value in data.items() if key != 'id'):
        return make_response(jsonify({"error": "All fields must be filled"}), 400)

    if 'year' in data:
        try:
            data["year"] = int(data.get("year"))
        except ValueError:
            return make_response(jsonify({"error": "Year must be an integer"}), 400)

    invalid_fields = [field for field in data if field not in MOVIE_FIELDS]
    if invalid_fields:
        return make_response(jsonify({"error": f"Invalid fields: {', '.join(invalid_fields)}"}), 400)

    movie = Movie.create(**data)
    new_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)


def update_movie(movie_id, data):
    """
    Update movie record by id
    """
    if not all(value for key, value in data.items() if key != 'id'):
        return make_response(jsonify({"error": "All fields must be filled"}), 400)

    if 'year' in data:
        try:
            data["year"] = int(data.get("year"))
        except ValueError:
            return make_response(jsonify({"error": "Year must be an integer"}), 400)

    invalid_fields = [field for field in data if field not in MOVIE_FIELDS]
    if invalid_fields:
        return make_response(jsonify({"error": f"Invalid fields: {', '.join(invalid_fields)}"}), 400)

    if not movie_id:
        return make_response(jsonify({"error": "ID should be specified"}), 400)

    if not isinstance(movie_id, int):
        return make_response(jsonify({"error": "ID must be an integer"}), 400)
    movie = Movie.query.get(movie_id)

    obj = Movie.query.filter_by(id=movie_id).first()
    if not obj:
        return make_response(jsonify({"error": "Record with such id does not exist"}), 400)

    if not movie:
        return make_response(jsonify({"error": "Movie not found"}), 404)

    upd_movie = Movie.update(movie_id, **data)
    new_movie = {k: v for k, v in upd_movie.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)


def delete_movie(movie_id):
    """
    Delete movie by id
    """
    if not isinstance(movie_id, int):
        return make_response(jsonify({"error": "ID must be an integer"}), 400)

    obj = Movie.query.filter_by(id=movie_id).first()
    if not obj:
        return make_response(jsonify({"error": "Record with such id does not exist"}), 400)

    if not movie_id:
        return make_response(jsonify({"error": "ID should be specified"}), 400)

    movie = Movie.query.get(movie_id)
    if not movie:
        return make_response(jsonify({"error": "Movie not found"}), 404)
    Movie.delete(movie_id)
    return make_response(jsonify({"message": "Movie deleted successfully"}), 200)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    movie_id = data.get('id')
    actor_id = data.get('relation_id')

    if not movie_id or not actor_id:
        return make_response(jsonify({"error": "ID and relation_id are required"}), 400)

    try:
        movie_id = int(movie_id)
        actor_id = int(actor_id)
    except ValueError:
        return make_response(jsonify({"error": "Both actor id and relation id must be integers"}), 400)

    movie = Movie.query.get(movie_id)

    if not movie:
        return make_response(jsonify({"error": "Movie with such id does not exist"}), 400)

    actor = Actor.query.get(actor_id)

    if not actor:
        return make_response(jsonify({"error": "Actor with such id does not exist"}), 400)

    rel_movie = Movie.add_relation(movie_id, actor)
    new_movie = {k: v for k, v in rel_movie.__dict__.items() if k in MOVIE_FIELDS}
    new_movie['cast'] = str(rel_movie.cast)
    return make_response(jsonify(new_movie), 200)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    movie_id = data.get('id')

    if not movie_id:
        return make_response(jsonify({"error": "No id specified"}), 400)

    try:
        movie_id = int(movie_id)
    except ValueError:
        return make_response(jsonify({"error": "Id must be integer"}), 400)

    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return make_response(jsonify({"error": "Record with such id does not exist"}), 400)

    rel_movie = Movie.clear_relations(movie_id)
    new_movie = {k: v for k, v in rel_movie.__dict__.items() if k in MOVIE_FIELDS}
    new_movie['cast'] = str(movie.cast)
    return make_response(jsonify(new_movie), 200)