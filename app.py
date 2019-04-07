from flask import Flask, render_template, request , redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime 

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/chukwuemekaonyebuchi/Desktop/FlaskWebBlog/blog.db' 
#os.environ.get('DATABASE_URL') or \
#'sqlite:///' + os.path.join(basedir, 'app.db')
#basedir = os.path.abspath(os.path.dirname(__file__))

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')

db_path = os.path.join(os.path.dirname(__file__), 'blog.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(30))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html',posts = posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%B %d,%Y')
    return render_template('post.html',post = post,date_posted= date_posted)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost',methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title= title, subtitle=subtitle, author=author, content=content,date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    #return '<h1>Title:{} Subtitle:{} Author:{} Content:{}</h1>'.format(title,subtitle,author,content)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)