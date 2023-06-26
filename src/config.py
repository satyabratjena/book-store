DEBUG = True
SECRET_KEY = "dev"
SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://postgres:password@localhost:5432/book_depot"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
