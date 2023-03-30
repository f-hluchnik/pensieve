import json
from flask import Flask, request, Response
from db.mongocrud import MongoCRUD
app = Flask(__name__)

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

@app.route('/getthoughts', methods=['GET'])
def getThoughts(count=1):
    """
    getThoughts ... Function returns n thoughts from the database. If no argument is given,
    function returns the standart set of 1 thought. You can provide an integer argument to
    specify how many thoughts you want.
    """
    db = MongoCRUD()
    response = db.read(count)
    return list(response)

@app.route('/getrandomthought', methods=['GET'])
def getRandomThought():
    """
    getThoughts ... Function returns a random thought from the database.
    """
    db = MongoCRUD()
    response = db.read_random()
    return list(response)

@app.route('/addthought', methods=['POST'])
def addThought(thought):
    """
    addThought ... Function adds one thought in the database. As input it expects a dictionary
    containing keys "thought" and "time".
    """
    db = MongoCRUD()
    response = db.write(thought)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

def updateThought(objectId, updatedThought):
    """
    updateThought ... Function updates one thought based on ObjectId. It expects objectId
    as a string and updatedThought as a dictionary as arguments.
    """
    db = MongoCRUD()
    response = db.update(objectId, updatedThought)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

def deleteThought(objectId):
    """
    updateThought ... Function updates one thought based on ObjectId. It expects objectId
    as a string and updatedThought as a dictionary as arguments.
    """
    db = MongoCRUD()
    response = db.delete(objectId)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# TODO: This function is just copied from the tutorial. Please update it before usage.
@app.route('/mongodb', methods=['GET'])
def mongo_read():
    obj1 = MongoCRUD()
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# TODO: This function is just copied from the tutorial. Please update it before usage.
@app.route('/mongodb', methods=['POST'])
def mongo_write():
    obj1 = MongoCRUD()
    response = obj1.write("")
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# TODO: This function is just copied from the tutorial. Please update it before usage.
@app.route('/mongodb', methods=['PUT'])
def mongo_update():
    obj1 = MongoCRUD()
    response = obj1.update('6410e29e7be95a9d841d591c')
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

# TODO: This function is just copied from the tutorial. Please update it before usage.
@app.route('/mongodb', methods=['DELETE'])
def mongo_delete():
    obj1 = MongoCRUD()
    response = obj1.delete("")
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
