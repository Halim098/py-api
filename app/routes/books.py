from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Book

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')

    book = Book(title=title, author=author, price=price)
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@books_bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'price': book.price} for book in books]), 200

@books_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.price = data.get('price', book.price)

    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200
