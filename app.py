import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.secret_key = "1234"


# главная страница
@app.route('/')
def index():
    return render_template('index.html')


# показываем все посты
@app.route('/posts')
def posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)


# отображаем каждый пост отдельно
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# переход на странцу каждого поста
@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post_id.html', post=post)


# создаем новую запись
@app.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)