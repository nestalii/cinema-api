from flask import jsonify, make_response
from flask import Flask, request
from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    # Отримання id з URL параметрів або тіла запиту
    actor_id = request.args.get('id') or get_request_data().get('id')

    if not actor_id:
        return make_response(jsonify(error='No id specified'), 400)

    try:
        row_id = int(actor_id)
    except ValueError:
        return make_response(jsonify(error='Id must be integer'), 400)

    obj = Actor.query.filter_by(id=row_id).first()
    if not obj:
        return make_response(jsonify(error='Record with such id does not exist'), 400)

    actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(actor), 200)

def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # use this for 200 response code
    if not all(field in data and data[field] for field in ACTOR_FIELDS if field != 'id'):
        return make_response(jsonify({"error": "All fields must be filled"}), 400)

    for field in data:
        if field not in ACTOR_FIELDS:
            return make_response(jsonify({"error": f"Invalid field: {field}"}), 400)

    if 'date_of_birth' in data:
        try:
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT)
        except ValueError:
            return make_response(jsonify({"error": f"Date of birth must be in format {DATE_FORMAT}"}), 400)

    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # use this for 200 response code
    if 'id' not in data:
        return make_response(jsonify({"error": "No id specified"}), 400)

    try:
        actor_id = int(data['id'])
    except ValueError:
        return make_response(jsonify({"error": "Id must be integer"}), 400)

    obj = Actor.query.filter_by(id=actor_id).first()
    if not obj:
        return make_response(jsonify({"error": "Record with such id does not exist"}), 400)

    for field in data:
        if field not in ACTOR_FIELDS:
            return make_response(jsonify({"error": f"Invalid field: {field}"}), 400)

    if 'date_of_birth' in data:
        try:
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT)
        except ValueError:
            return make_response(jsonify({"error": f"Date of birth must be in format {DATE_FORMAT}"}), 400)

    upd_record = Actor.update(actor_id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)
    ### END CODE HERE ###


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # use this for 200 response code
    if 'id' not in data:
        return make_response(jsonify({"error": "No id specified"}), 400)

    try:
        actor_id = int(data['id'])
    except ValueError:
        return make_response(jsonify({"error": "Id must be integer"}), 400)

    deleted = Actor.delete(actor_id)
    if not deleted:
        msg = 'Record with such id does not exist'
        return make_response(jsonify(message=msg), 400)
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # use this for 200 response code
    actor_id = data.get('id')
    relation_id = data.get('relation_id')

    if not actor_id or not relation_id:
        return make_response(jsonify({"error": "Both actor id and relation id must be specified"}), 400)

    try:
        actor_id = int(actor_id)
        relation_id = int(relation_id)
    except ValueError:
        return make_response(jsonify({"error": "Both actor id and relation id must be integers"}), 400)

    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        return make_response(jsonify({"error": "Actor with such id does not exist"}), 400)

    movie = Movie.query.filter_by(id=relation_id).first()
    if not movie:
        return make_response(jsonify({"error": "Movie with such id does not exist"}), 400)

    actor = Actor.add_relation(actor_id, movie) # add relation here
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # use this for 200 response code
    actor_id = data.get('id')

    if not actor_id:
        return make_response(jsonify({"error": "No id specified"}), 400)

    try:
        actor_id = int(actor_id)
    except ValueError:
        return make_response(jsonify({"error": "Id must be integer"}), 400)

    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        return make_response(jsonify({"error": "Record with such id does not exist"}), 400)

    actor = Actor.clear_relations(actor_id) # clear relations here
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
    ### END CODE HERE ###