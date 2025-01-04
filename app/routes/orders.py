from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, Book

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    current_user = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')

    book = Book.query.get_or_404(book_id)
    order = Order(user_id=current_user['id'], book_id=book.id)

    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    current_user = get_jwt_identity()
    orders = Order.query.filter_by(user_id=current_user['id']).all()
    return jsonify([{'id': order.id, 'book_title': order.book.title, 'order_date': order.order_date} for order in orders]), 200
