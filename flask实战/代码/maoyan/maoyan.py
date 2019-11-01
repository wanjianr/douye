from flask import Flask, render_template, redirect, url_for,request,session
from flask_sqlalchemy import SQLAlchemy

from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/flaskweb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)

class User(db.Model): # 继承数据库模型类
    # 设置表名
    __tablename__ = 'user' 
    # 设置字段
    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    name = db.Column(db.String(16), nullable=False, unique = True)
    passward = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(48), nullable=False)

class MaoyanTop100(db.Model):
    __tablename__ = 'maoyan'

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, index=True, unique = True)
    pic_url = db.Column(db.String(128))
    name = db.Column(db.String(64))
    actors = db.Column(db.String(128))
    time = db.Column(db.String(64))
    intro = db.Column(db.String(1024))
    site = db.Column(db.String(64))
    prize_url = db.Column(db.String(256))
    prize_name = db.Column(db.String(64))
    prize_content = db.Column(db.String(1024))

class Comment(db.Model): # 继承数据库模型类
    # 设置表名
    __tablename__ = 'comment' 
    # 设置字段
    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer,db.ForeignKey('maoyan.id'))

    user_comment = db.relationship("User",backref=db.backref('comments'))
    movie_comment = db.relationship("MaoyanTop100",backref=db.backref('comments',order_by=create_time.desc()))

def login_require(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/<int:page>')
def index(page):
    film = MaoyanTop100.query.order_by('rank').paginate(page=page,per_page=8)
    row_li = []
    film_li = []
    for movie in film.items:
        row_li.append(movie)
        if len(row_li) == 2:
            film_li.append(row_li)
            row_li = []
    return render_template('index.html', film = film_li, film_index = film)

@app.route('/update')
def update():
    os.chdir(r'/home/www/maoyan/mySpider/mySpider/spiders/')
    os.system('scrapy crawl maoyan')
    os.chdir('/home/www/maoyan/')
    return redirect(url_for('index',page=1))

@app.route('/search',methods=['POST'])
def search():
    search_key = request.form.get('search')
    
    search_movie = MaoyanTop100.query.filter(MaoyanTop100.name == search_key).first()
    if search_movie:
        return redirect(url_for('detail',movie_id=search_movie.id))
    else:
        return redirect(url_for('index',page=1))

@app.route('/comment',methods=['POST'])
@login_require
def add_comment():
    content = request.form.get('add_comment')
    movie_id = request.form.get('movie_id')
    comment = Comment(content=content)
    user_id = session['user_id']
    comment.author_id = user_id
    comment.movie_id = movie_id
    user = User.query.filter(User.id==user_id).first()
    movie = MaoyanTop100.query.filter(MaoyanTop100.id==movie_id).first()
    comment.user_comment = user
    comment.movie_comment = movie
    db.session.add(comment)
    db.session.commit()  

    return redirect(url_for('detail',movie_id=movie_id))

@app.route('/detail/<int:movie_id>',methods=['GET','POST'])
def detail(movie_id):
    movie = MaoyanTop100.query.filter(MaoyanTop100.id == movie_id).first() 
    prize_name = eval(movie.prize_name)
    prize_url = eval(movie.prize_url)
    prize_content = eval(movie.prize_content)
    prize_num = len(prize_name)
    num = len(movie.comments)
    # content = {'movie':movie, 'num':num, 'prize_url':prize_url,'prize_name':prize_name, 'prize_content':prize_content}     
    return render_template('detail.html',movie=movie, prize_num=prize_num, num=num, prize_url=prize_url,prize_name=prize_name, prize_content=prize_content)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('name')
        passward = request.form.get('pwd')

        if not all([username,passward]):
            error = 'Username and password cannot be empty!'
            return render_template('login.html',error_info=error)
        user = User.query.filter(User.name == username,User.passward == passward).first()

        if user:
            session['user_id'] = user.id
            # session.permanent = True
            return redirect(url_for('index',page=1))
        else:
            error = 'username or passward error!'
            return render_template('login.html',error_info=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('user_name')
        passward1 = request.form.get('pwd')
        passward2 = request.form.get('cpwd')
        email = request.form.get('email')

        user_ = User.query.filter(User.name == username).first()
        email_ = User.query.filter(User.email == email).first()

        if not all([username,passward1,passward2,email]):
            error = 'Registration information is incomplete!'
            return render_template('register.html',error_info=error)

        if user_ or email_:
            error = 'username or email is exist!'
            return render_template('register.html',error_info=error)
        else:
            if passward1 == passward2:
                u = User(name=username,passward=passward1,email=email)
                db.session.add(u)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                error = 'passward is not consistant!'
                return render_template('register.html',error_info=error)

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run(debug=True)
