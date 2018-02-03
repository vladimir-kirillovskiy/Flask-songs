from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

from custom_decorators import crossdomain

app = Flask(__name__)

app.config['MONGO_DB_NAME'] = 'rest_api'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/rest_api'

mongo = PyMongo(app)

@app.route('/')
@crossdomain(origin='*')
def index():
    return "Welcome to the song api app "

# List all the songs
@app.route('/songs', methods=['GET'])
@crossdomain(origin='*')
def songs():
    songs = mongo.db.songs

    if request.args.get('limit') is not None and request.args.get('offset') is not None:
        limit = int(request.args.get('limit'))
        offset = int(request.args.get('offset'))
    else:
        limit = 4
        offset = 0

    output = []
    count = songs.count()

    for q in songs.find().skip(offset).limit(limit):
        output.append({
            'song_id': str(q['_id']),
            'title': q['title'], 
            'artist': q['artist'],
            'difficulty': q['difficulty'],
            'level': q['level'],
            'released': q['released']
        })

    return jsonify({'result': output, 'count': count, 'offset': offset})

# Show average difficulty for all songs
# or if parameter level is given list all the songs given difficulty
@app.route('/songs/avg/difficulty', methods=['GET'])
@crossdomain(origin='*')
def avg_difficulty():
    songs = mongo.db.songs
    level = request.args.get('level', type = int)
    output = []

    # if there is valid level show all songs of that level
    if level is not None and level > 0:
        for q in songs.find({'level': level}):
            output.append({
                'song_id': str(q['_id']),
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
        result = list(songs.aggregate(pipeline = pipe))
        return jsonify({'result': result[0]['avg']})

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
                'song_id': str(q['_id']),
                'title': q['title'], 
                'artist': q['artist'],
                'difficulty': q['difficulty'],
                'level': q['level'],
                'released': q['released']
            })

        return jsonify({'result': output})
    else:
        return jsonify({'result': 'No message string is received'})

# Add rating to the song, 1-5
@app.route('/songs/rating', methods=['POST'])
@crossdomain(origin='*')
def songs_rating():
    ratings = mongo.db.ratings
    song_id = request.form['song_id']
    rating = int(request.form['rating'])

    output = []

    if rating > 0 and rating < 6:
        # add rating value
        ratings.insert({
            'song_id': ObjectId(song_id),
            'rating': rating
        })

        return jsonify({'result': 'Rating Added'})
    else:
        return jsonify({'result': 'Rating should be between 1 and 5'})

# Returns the average, the lowest and the highest rating of the given song id
@app.route('/songs/avg/rating/<song_id>', methods=['GET'])
@crossdomain(origin='*')
def get_song_rating(song_id):
    ratings = mongo.db.ratings

    output = {
        'avg': 0,
        'min': 0,
        'max': 0
    }

    pipe = [
            {'$match': {'song_id': ObjectId(song_id)}},
            {'$unwind': '$rating'},
            {'$group': {
                '_id': "null", 
                "avg": {'$avg': '$rating'},
                "min": {'$min': '$rating'},
                "max": {'$max': '$rating'},
            }}
        ]

    result = list(ratings.aggregate(pipeline = pipe))

    if len(result) > 0:
        output = {
            'avg': result[0]['avg'],
            'min': result[0]['min'],
            'max': result[0]['max']
        }
        return jsonify({'result': output})

    return jsonify({'result': output})

if __name__ == "__main__":
    app.run(debug=True)