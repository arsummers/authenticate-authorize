from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import User, Author, Book
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    data = [user.to_dict() for user in User.query.all()]
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')

    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')

    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}

    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')

    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/ping')
@token_auth.login_required
def ping():
    return 'pong'


# NOTE: again, not sure how to add stuff from these to database, or how they should interact with the rest.

@bp.route('/authors', methods=['GET'])
def all_authors():
        authors = [author.to_dict() for author in Author.query.all()]
        return jsonify(authors)

@bp.route('/books', methods=['GET'])
def all_books():
        books = [book.to_dict() for book in Book.query.all()]
        return jsonify(books)
