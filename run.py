from app import create_app, db
from models import User

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run()
