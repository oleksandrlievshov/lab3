from flask import Flask
from .routes import book_bp
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(book_bp, url_prefix="/api/books")

    with app.app_context():
        db.create_all()

    return app