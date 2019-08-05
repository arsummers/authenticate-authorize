from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import User, Author
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/authors/<int:id>', methods=['GET'])
@token_auth.login_required
def get_author(id):
    return jsonify(Author.query.get_or_404(id).to_dict())

@bp.route('/authors', methods=['GET'])
@token_auth.login_required
def get_authors():
    data = [author.to_dict() for author in Author.query.all()]
    return jsonify(data)

@bp.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username, password fields')

    if Author.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')


    author = Author()
    author.from_dict(data, new_user=True)
    db.session.add(author)
    db.session.commit()
    response = jsonify(author.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_author', id=author.id)
    return response


@bp.route('/authors/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_author(id):
    if g.current_user.id != id:
        abort(403)
    author = Author.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != author.username and \
            Author.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')

    author.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(author.to_dict())