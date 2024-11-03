from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message  # Ensure this import is correct

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        return jsonify([msg.to_dict() for msg in messages]), 200
    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # Update this line to use db.session.get() instead of Query.get()
    message = db.session.get(Message, id)
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    if request.method == 'PATCH':
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict()), 200
    
    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted"}), 204
