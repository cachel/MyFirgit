#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager, current_user, login_user, login_required, UserMixin,logout_user
from werkzeug.utils import secure_filename
from PathConfig import basedpath
from dao.ReadAndWriteJson import IndexPageInfoDao

web_app = Flask(__name__)
web_app.secret_key = '123'
login_manager = LoginManager()
login_manager.init_app(web_app)
login_manager.login_view = "login"  # 定义登录的 视图
login_manager.login_message = '请登录以访问此页面'  # 定义需要登录访问页面的提示消息

users = {'foo@bar.tld': {'password': 'secret'}}

ipid = IndexPageInfoDao(basedpath)

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

class User(UserMixin):
    pass


@web_app.route('/detail')
def indexn():
    name = request.args.get('name')
    detailImages = ipid.getSpecifiedDetailInfo(name)
    return render_template('detail.html',
                           title='detail',
                           detailImages = detailImages)


@web_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    print(email)
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@web_app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

@web_app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

@web_app.route('/test')
def test():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("test.html",
                           title='',
                           user=user,
                           posts=posts)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return '''
                   <form action='../login' method='POST'>
                    <input type='text' name='email' id='email' placeholder='email'/>
                    <input type='password' name='password' id='password' placeholder='password'/>
                    <input type='submit' name='submit'/>
                   </form>
                   '''

@web_app.route('/upload', methods=['POST', 'GET'])
def upload():
     if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static','upload',secure_filename(f.filename))
        #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('upload'))
     return render_template('upload.html')


@web_app.route('/', methods=['GET'])
def haha():
    portfolioImagesInfo = ipid.getIndexPageImageDetailArray()

    return render_template("index.html",
                           title='index',
                           portfolioImages=portfolioImagesInfo)


# start command : uwsgi --http :9090 --wsgi-file FlaskWeb.py --callable web_app --master --processes 4 --threads 2 --stats 127.0.0.1:9191
application = web_app.wsgi_app

if __name__ == '__main__':
    web_app.run(debug=True,port=8080)