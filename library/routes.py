from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from .schemas import BookSchema
from .models import Book, db

book_bp = Blueprint("books", __name__)
book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

@book_bp.route("/", methods=["GET"])
def get_books():
    try:
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit та offset мають бути числами"}), 400

    books = Book.query.offset(offset).limit(limit).all()
    return jsonify(book_list_schema.dump(books)), 200

@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Книгу не знайдено"}), 404
    return jsonify(book_schema.dump(book)), 200

@book_bp.route("/", methods=["POST"])
def add_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    book = Book(**book_data)
    db.session.add(book)
    db.session.commit()
    return jsonify(book_schema.dump(book)), 201

@book_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Книгу не знайдено"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Книгу видалено"}), 200