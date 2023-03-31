import json
from flask import Flask, Response
from db.mongocrud import MongoCRUD
app = Flask(__name__)
db = MongoCRUD()

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

@app.route('/getthoughts', methods=['GET'])
def getThoughts(query={}, count=1, hashtags=[]):
    """
    getThoughts ... Function returns n thoughts from the database based on provided query,
    count and hashtags. The thouhts are sorted in descending order based on 'timestamp_real'
    field.
    """
    if len(hashtags) > 0:
        query = {'hashtags': {'$all': hashtags}}
    response = db.read(query, limit=count)
    return list(response)

@app.route('/getrandomthought', methods=['GET'])
def getRandomThought():
    """
    getRandomThought ... Function returns a random thought from the database.
    """
    response = db.read_random()
    if len(response) > 0:
        return response[0]
    else:
        return {"", "0"}

@app.route('/getlasttimestamp', methods=['GET'])
def getLastTimestamp():
    """
    getLastTimestamp ... Function returns the real timestamp of the last item inserted in the database.
    """
    response = db.read(limit=1)
    if len(response) >= 1:
        return response[0]["timestamp_real"]
    else:
        return 0

@app.route('/addthought', methods=['POST'])
def addThought(thought):
    """
    addThought ... Function adds one thought in the database. As input it expects a dictionary
    containing keys "thought", "timestamp_print" and "timestamp_real".
    """
    response = db.write(thought)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/addthoughts', methods=['POST'])
def addThoughts(thoughts):
    """
    addThoughts ... Function adds thoughts in the database. As input it expects a list of dictionaries
    containing keys "thought", "timestamp_print" and "timestamp_real".
    """
    response = db.write_many(thoughts)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

def updateThought(objectId, updatedThought):
    """
    updateThought ... Function updates one thought based on ObjectId. It expects objectId
    as a string and updatedThought as a dictionary as arguments.
    """
    response = db.update(objectId, updatedThought)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

def deleteThought(objectId):
    """
    updateThought ... Function updates one thought based on ObjectId. It expects objectId
    as a string and updatedThought as a dictionary as arguments.
    """
    response = db.delete(objectId)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
