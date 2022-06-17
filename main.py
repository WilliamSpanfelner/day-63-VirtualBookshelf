from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# all_books = []

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book: {self.title}>"


@app.route('/')
def home():
    try:
        all_books = Books.query.all()
    except:
        db.create_all()
        all_books = Books.query.all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # book = {
        #     "title": request.form['title'],
        #     "author": request.form['author'],
        #     "rating": request.form['rating'],
        # }
        # all_books.append(book)
        next_index = len(Books.query.all()) + 1
        book = Books(id=next_index,
                     title=request.form['title'],
                     author=request.form['author'],
                     rating=float(request.form['rating']),
                     )
        db.session.add(book)
        db.session.commit()

        all_books = Books.query.all()
        print(all_books)

        return redirect(url_for("home"))
    return render_template('add.html')


@app.route("/update/<book_id>", methods=['GET', 'POST'])
def update(book_id):
    if request.method == 'POST':
        new_rating = request.form.get('new_rating')
        book_to_update = Books.query.get(book_id)
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))
    book_to_update = Books.query.get(book_id)
    return render_template('edit_rating.html', book=book_to_update)


@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get('username')
    print(username)
    password = request.form.get('password')
    print(password)
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
