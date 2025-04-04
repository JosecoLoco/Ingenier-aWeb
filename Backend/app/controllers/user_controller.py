from app import db
from app.models.user import User
from flask import jsonify

def create_user(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {'message': 'Faltan campos requeridos'}, 400

    if User.query.filter_by(username=username).first():
        return {'message': 'El nombre de usuario ya existe'}, 400

    if User.query.filter_by(email=email).first():
        return {'message': 'El correo electrónico ya existe'}, 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'Usuario registrado exitosamente'}, 201

def get_all_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(user_list), 200

def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200

def update_user(user_id, data):
    user = User.query.get_or_404(user_id)
    username = data.get('username')
    email = data.get('email')

    if username:
        if User.query.filter(User.username == username, User.id != user_id).first():
            return {'message': 'El nombre de usuario ya existe'}, 400
        user.username = username
    if email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return {'message': 'El correo electrónico ya existe'}, 400
        user.email = email
    if 'password' in data and data['password']:
        user.set_password(data['password'])

    db.session.commit()
    return {'message': 'Usuario actualizado exitosamente'}, 200

def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {'message': 'Usuario eliminado exitosamente'}, 200

def login_user(data):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {'message': 'Faltan campos requeridos'}, 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return {'message': 'Inicio de sesión exitoso', 'user_id': user.id, 'username': user.username}, 200
    else:
        return {'message': 'Credenciales inválidas'}, 401