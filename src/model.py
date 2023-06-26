from src import db
from dataclasses import dataclass
from marshmallow import Schema, fields



print("Creator")
@dataclass
class Book(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    author: str = db.Column(db.String(100), nullable=False)
    country: str = db.Column(db.String(100), nullable=False)
    imageLink: str = db.Column(db.String(100), nullable=True)
    language: str = db.Column(db.String(100), nullable=False)
    link: str = db.Column(db.String(100), nullable=True)
    pages: int = db.Column(db.Integer, nullable=True)
    title: str = db.Column(db.String(100), nullable=False)
    year: int = db.Column(db.Integer, nullable=False)
    # print("yearend")

class BookSchema(Schema):
    id = fields.Integer()
    author = fields.String()
    country = fields.String()
    imageLink = fields.String()
    language = fields.String()
    link = fields.String()
    pages = fields.Integer()
    title = fields.String()
    year = fields.Integer()


# # class BookSchema(Schema):
# #     class Meta:
# #         fields = ("author", "country", "imagelink", "language", "title", "year")

# from flask_marshmallow import Marshmallow
# class BookSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Book
#         include_fk = True
#         exclude = ["id"]

books = BookSchema()
book_many = BookSchema(many=True)

