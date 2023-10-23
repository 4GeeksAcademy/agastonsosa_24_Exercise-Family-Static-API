import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Body is required'}), 400 
    if 'first_name' not in body:
        return jsonify({'msg':'first_name field in body required'}), 400
    if 'age' not in body:
        return jsonify({'msg':'age field in body required'}), 400
    if 'lucky_numbers' not in body:
        return jsonify({'msg':'lucky_numbers field in body required'}), 400
    id_member = jackson_family._generateId()
    if 'id' in body:
        id_member = body['id']
    new_member = {
        'id': id_member,
        'first_name': body['first_name'],
        'last_name': jackson_family.last_name,
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers']
    }
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    if member:
        return jsonify({'done': True}), 200
    else:
        return jsonify({'error': 'Member not found'}), 404

@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Body is required'}), 400 
    updated_member = jackson_family.update_member(id, body)
    if updated_member:
        return jsonify(updated_member), 200
    else:
        return jsonify({'error': 'Member not found'}), 404

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    else:
        return jsonify(member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
