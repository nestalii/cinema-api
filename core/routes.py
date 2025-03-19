from flask import Flask, request
from flask import current_app as app

from controllers.actor import *
from controllers.movie import *


@app.route('/api/actors', methods=['GET'])
def actors():
    """
 Get all actors in db
	"""
    return get_all_actors()


@app.route('/api/movies', methods=['GET'])
def movies():
    """
 Get all movies in db
	"""
    return get_all_movies()


@app.route('/api/actor', methods=['GET', 'POST', 'PUT', 'DELETE'])
def actor():
    if request.method == 'GET':
        return get_actor_by_id()
    elif request.method == 'POST':
        return add_actor()
    elif request.method == 'PUT':
        data = get_request_data()
        actor_id = data.get('id')
        if actor_id:
            return update_actor()
        return make_response(jsonify({"error": "ID is required"}), 400)
    elif request.method == 'DELETE':
        data = get_request_data()
        actor_id = data.get('id')
        if actor_id:
            return delete_actor()
        return make_response(jsonify({"error": "ID is required"}), 400)

@app.route('/api/movie', methods=['GET', 'POST', 'PUT', 'DELETE'])
def movie():
    if request.method == 'GET':
        return get_movie_by_id()
    elif request.method == 'POST':
        return add_movie()
    elif request.method == 'PUT':
        data = get_request_data()
        movie_id = data.get('id')
        if movie_id:
            return update_movie(int(movie_id), data)
        return make_response(jsonify({"error": "ID is required"}), 400)
    elif request.method == 'DELETE':
        data = get_request_data()
        movie_id = data.get('id')
        if movie_id:
            return delete_movie(int(movie_id))
        return make_response(jsonify({"error": "ID is required"}), 400)


@app.route('/api/actor-relations', methods=['PUT', 'DELETE'])
def actor_relation():
    if request.method == 'PUT':
        return actor_add_relation()
    elif request.method == 'DELETE':
        return actor_clear_relations()


@app.route('/api/movie-relations', methods=['PUT', 'DELETE'])
def movie_relation():
    if request.method == 'PUT':
        return movie_add_relation()
    elif request.method == 'DELETE':
        return movie_clear_relations()