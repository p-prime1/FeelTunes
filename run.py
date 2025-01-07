from app import create_app, db
from models import User
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(host="0.0.0.0", port=port)
