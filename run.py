from app import create_app
from models import User

app = create_app()

if __name__ == "__main__":
# Create database tables
    app.run(debug=True)
