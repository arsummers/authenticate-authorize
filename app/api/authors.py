from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import User, Author, Book
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@bp.route('/authors/<int:id>', methods=['GET'])
