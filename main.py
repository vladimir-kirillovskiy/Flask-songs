from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

# TODO: move to another file
# Custom decorator to allow cross domain api calls
# https://stackoverflow.com/questions/22181384/javascript-no-access-control-allow-origin-header-is-present-on-the-requested
# http://flask.pocoo.org/snippets/56/
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


app = Flask(__name__)

app.config['MONGO_DB_NAME'] = 'rest_api'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/rest_api'

mongo = PyMongo(app)

@app.route('/')
def index():
    return "Welcome to the song api app "

# List all the songs
@app.route('/songs', methods=['GET'])
def songs():
    # TODO: add pagination
    # options: page, number of songs
    songs = mongo.db.songs
    output = []

    for q in songs.find():
        output.append({
            'id': str(q['_id']),
            'title': q['title'], 
            'artist': q['artist'],
            'difficulty': q['difficulty'],
            'level': q['level'],
            'released': q['released']
        })

    return jsonify({'result': output})

# Show average difficulty for all songs
# or if parameter level is given list all the songs given difficulty
@app.route('/songs/avg/difficulty', methods=['GET'])
def avg_difficulty():
    songs = mongo.db.songs
    level = request.args.get('level', type = int)
    output = []

    # if there is valid level show all songs of that level
    if level is not None and level > 0:
        for q in songs.find({'level': level}):
            output.append({
                'title': q['title'], 
                'artist': q['artist'],
                'difficulty': q['difficulty'],
                'level': q['level'],
                'released': q['released']
            })
        return jsonify({'result': output})
    else:   # if not return average for all songs
        pipe = [
            {'$unwind': '$level'},
            {'$group': {'_id': "null", "avg": {'$avg': '$level'}}}
        ]
        result = songs.aggregate(pipeline = pipe)
        return jsonify({'result': list(result)[0]['avg']})

# Search for the songs over artist and title
@app.route('/songs/search', methods=['GET'])
@crossdomain(origin='*')
def song_search():
    songs = mongo.db.songs
    message = request.args.get('message')
    output = []

    # Search using regex
    if message is not None:
       
        for q in songs.find({'$or': [
            {'title': {'$regex': message, '$options': ''}},
            {'artist': {'$regex': message, '$options': ''}
        }]}):
            output.append({
                'title': q['title'], 
                'artist': q['artist'],
                'difficulty': q['difficulty'],
                'level': q['level'],
                'released': q['released']
            })

        return jsonify({'result': output})
    else:
        return "No message string is received"

# Add rating to the song, 1-5
@app.route('/songs/rating', methods=['POST'])
def songs_rating():
    songs = mongo.db.songs

    song_id = request.json['song_id']
    rating = request.json['rating']

    output = []

    # add rating value
    # for the next task we need average, min and max for rating field
    # that means to one to many relations
    # songs.update({'_id': ObjectId(song_id)}, {'$set': {'rating': rating}})

    # for q in songs.find({'_id': ObjectId(song_id)}):
    #     output.append({
    #         'title': q['title'], 
    #         'artist': q['artist'],
    #         'difficulty': q['difficulty'],
    #         'level': q['level'],
    #         'released': q['released'],
    #         'rating': q['rating']
    #     })

    # return jsonify({'result': output})
    return "Done it wrong!"

# Returns the average, the lowest and the highest rating of the given song id
@app.route('/songs/avg/rating/<song_id>', methods=['GET'])
def get_song_rating(song_id):
    # songs = mongo.db.songs

    # pipe = [
    #         {'$unwind': '$rating'},
    #         {'$group': {
    #             '_id': "null", 
    #             "avg": {'$avg': '$rating'},
    #             "min": {'$min': '$rating'},
    #             "max": {'$max': '$rating'},
    #         }}
    #     ]
    # result = songs.aggregate(pipeline = pipe)
    # return jsonify({'result': list(result)[0]['avg']})

    return "in progress"

if __name__ == "__main__":
    app.run(debug=True)