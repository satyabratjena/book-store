import requests
import urllib, json
from src.model import db, Book
# from src import create_app

# app = create_app()

def load_json():
    # with app.app_context():
    
        with open("bin/books.json", 'r') as file:
            json_data = json.load(file)
    
        for item in json_data:
            # present_book = Book.query.filter_by(title=item.get("title")).first()

            # # print(present_book)     
            # if present_book:
            #    return {"error": "Book title already present"}
            
            book = Book(
                # see how can i use schema to do this or using **kwargs
                author=item.get("author"),
                country=item.get("country"),
                imageLink=item.get("imageLink"),
                language=item.get("language"),
                link=item.get("link"),
                pages=item.get("pages"),
                title=item.get("title"),
                year=item.get("year"),
            )
            db.session.add(book)
            db.session.commit()
    
        return {"success": True, "message": "data inserted successfully"}

# load_json("bin/books.json")        



# def load_json():

#     url = "https://github.com/benoitvallon/100-best-books/blob/master/books.json"
#     response = requests.get(url)
#     print(response)
#     json_data = response.json()
#     for item in json_data:
#          present_book = Book.query.filter_by(title=item.get("title")).first()
#          if present_book:
#              return {"error": "Book title already present"}
#          book = Book(
#             # see how can i use schema to do this or using **kwargs
#             author=item.get("author"),
#             country=item.get("country"),
#             imageLink=item.get("imageLink"),
#             language=item.get("language"),
#             link=item.get("link"),
#             pages=item.get("page"),
#             title=item.get("title"),
#             year=item.get("year"),
#         )
#     db.session.add(book)
#     db.session.commit()
#     return {"success": True, "message": "data inserted successfully"}

# load_json()
# def load_book_data():
#     # Parsing the JSON data and creating model instances
#     url = "https://github.com/benoitvallon/100-best-books/blob/master/books.json"
#     response = requests.get(url)
#     json_data = response.json()
#     # Parse the JSON data and map it to your database model
#     for item in json_data:
#         present_book = Book.query.filter_by(name=item.get("title")).first()
#         if present_book:
#             return {"error": "Book title already present"}
#         book = Book(
#             # see how can i use schema to do this or using **kwargs
#             author=item.get("author"),
#             country=item.get("country"),
#             imageLink=item.get("imageLink"),
#             language=item.get("language"),
#             link=item.get("link"),
#             page=item.get("page"),
#             title=item.get("title"),
#             year=item.get("year"),
#         )
#         db.session.add(book)
#     db.session.commit()


# load_book_data()