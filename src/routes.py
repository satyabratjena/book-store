
from flask import Blueprint, request, url_for
# from src import create_app
from src.model import Book,db
from bin.load_url import load_json

# app = create_app()

book_api = Blueprint("book_api", __name__, url_prefix="/v1/books")

# Below are custom error handlers
class ValueError(Exception):
    def __init__(self, error, code=400):
        self.error = error
        self.code = code

@book_api.errorhandler(ValueError)
def data_already_exists(e):
    return {
        "error": f"Not Found: {e}",
        "message" : "The requested query could not be found"
    }

# print("book_api")
@book_api.route("/", methods=["GET"])
def index(book_id=None):
    """
    This API method returns a list of all information related to books and manual
    search results to get a list of specific information.
    
    """
    
    author = request.args.get("author")
    country = request.args.get("country")
    language = request.args.get("language")
    title = request.args.get("title")
    year = request.args.get("year")
    min_pages = request.args.get("min_pages")
    sort = request.args.get("sort", "author")
    order = request.args.get("order", "asc")
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    
    query = Book.query
    if book_id:
        query = query.filter(Book.id == book_id)
        if not query:
            raise ValueError("Id does not exist", 404)

    query = query.order_by(getattr(getattr(Book, sort), order)())

    if author:
        author = author.capitalize()
        query = query.filter(Book.author.startswith("author"))
    if country:
        country = country.capitalize()
        query = query.filter(Book.country.startswith("country"))
    if language:
        language = language.capitalize()
        query = query.filter(Book.language.ilike(f"%{language}%"))
    if min_pages:
        min_pages = int(min_pages)
        query = Book.query.filter(Book.pages >= min_pages).all()
    if title:
        title = Book.title
    return {"success": True}

# Below is for loading the data to table

@book_api.route("/load_url_data", methods=["POST"])
def load_url_data():
    json_data = load_json() 
    return json_data


@book_api.route("/",methods=["POST"])
def create_book():
    book_data = request.json
    return "save book"

@book_api.route("/<id>",methods=["DELETE"])
@book_api.route("/",methods=["DELETE"])
def delete_book(id=None):
    if id:
        book = Book.query.filter_by(id=id).first()
        if not book:
            return {"success": False, "error": "Book not found"}
        db.session.delete(book)
        db.session.commit()
        return {"success": True, "error": "Book deleted successfully"}
    else:
        db.session.query(Book).delete()
        db.session.commit()
        return {"success": True, "error": "Book deleted successfully"}

        
    


