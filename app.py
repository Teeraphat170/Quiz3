from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SECRET_KEY'] = "secret-key"

db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = "books"
 
    title = db.Column(db.String(), primary_key=True)
    author = db.Column(db.String())
    genre = db.Column(db.String())
    height = db.Column(db.Integer())
    publisher = db.Column(db.String())

@app.route('/')
def home():
   return render_template('home.html', books = Books.query.all() )


@app.route('/insert', methods=["GET", "POST"])
def insert():
    if request.method == 'GET':
        return render_template("insert.html")
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        height = request.form['height']
        publisher = request.form['publisher']
        book = Books(title=title, author=author, genre=genre, height=height, publisher=publisher)
        db.session.add(book)
        db.session.commit()
        return redirect('/')


@app.route('/update/<string:title>', methods=["GET", "POST"])
def update(title):
    book = Books.query.get_or_404(title)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.height = request.form['height']
        book.publisher = request.form['publisher']
        try : 
            db.session.commit()
            return redirect('/')
        except :
            return "Fail to update"
    else :
        return render_template("update.html", book=book)

@app.route('/delete/<string:title>', methods=["GET", "POST"])
def delete(title):
    book = Books.query.filter_by(title=title).first()
    if request.method == 'GET':
        if book:
            db.session.delete(book)
            db.session.commit()
            return redirect('/')

app.env="development"
app.run(debug=True)
