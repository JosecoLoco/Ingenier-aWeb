# app/views/user_views.py
from flask import Blueprint, request, jsonify
from app.controllers import user_controller

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status_code = user_controller.create_user(data)
    return jsonify(response), status_code

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status_code = user_controller.login_user(data)
    return jsonify(response), status_code

@bp.route('/', methods=['GET'])
def get_users():
    response, status_code = user_controller.get_all_users()
    return response, status_code

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    response, status_code = user_controller.get_user(user_id)
    return response, status_code

@bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    response, status_code = user_controller.update_user(user_id, data)
    return jsonify(response), status_code

@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    response, status_code = user_controller.delete_user(user_id)
    return jsonify(response), status_code