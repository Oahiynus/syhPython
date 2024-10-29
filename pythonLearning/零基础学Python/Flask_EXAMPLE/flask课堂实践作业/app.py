from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话加密的密钥，请替换为实际密钥

DATABASE = 'E:\\YNU\\5\\Python\\syhPython\\PythonLearning\\零基础学Python\\Flask_example\\flask课堂实践作业\\users.db'

def init_db():
    # 仅在数据库文件不存在时初始化
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # 创建用户表
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            # 创建笔记表
            cursor.execute('''
                CREATE TABLE notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            # 创建帖子表
            cursor.execute('''
                CREATE TABLE posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            # 创建回复表
            cursor.execute('''
                CREATE TABLE replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    user_id INTEGER,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES posts (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            # 添加一个默认用户
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('syh', '123456'))
            conn.commit()


def get_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
    return user

def get_notes(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM notes WHERE user_id = ?', (user_id,))
        notes = [note[0] for note in cursor.fetchall()]  # 提取内容
    return notes

def add_note(user_id, content):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (user_id, content) VALUES (?, ?)', (user_id, content))
        conn.commit()

def register_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # 检查两次密码输入是否一致
        if password != confirm_password:
            flash('密码不匹配，请重新输入。', 'danger')
            return render_template('register.html')

        # 检查用户名是否已存在
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                flash('用户名已存在，请选择其他用户名。', 'danger')
                return render_template('register.html')
        
        # 注册新用户
        register_user(username, password)
        flash('注册成功，请登录。', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

def get_all_posts():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # 获取所有帖子及其回复
        cursor.execute('''
            SELECT posts.id, posts.content, posts.created_at, users.username
            FROM posts
            JOIN users ON posts.user_id = users.id
            ORDER BY posts.created_at DESC
        ''')
        posts = cursor.fetchall()
        
        # 获取每个帖子的回复
        post_data = []
        for post in posts:
            cursor.execute('''
                SELECT replies.content, replies.created_at, users.username
                FROM replies
                JOIN users ON replies.user_id = users.id
                WHERE replies.post_id = ?
                ORDER BY replies.created_at ASC
            ''', (post['id'],))
            replies = cursor.fetchall()
            post_data.append({
                'id': post['id'],
                'content': post['content'],
                'created_at': post['created_at'],
                'username': post['username'],
                'replies': replies
            })
    return post_data

from datetime import datetime, timedelta

def add_post(user_id, content):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # 获取当前时间并转换为东八区时间，只保留到秒
        current_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO posts (user_id, content, created_at) VALUES (?, ?, ?)', 
                       (user_id, content, current_time))
        conn.commit()

def add_reply(post_id, user_id, content):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # 获取当前时间并转换为东八区时间，只保留到秒
        current_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO replies (post_id, user_id, content, created_at) VALUES (?, ?, ?, ?)', 
                       (post_id, user_id, content, current_time))
        conn.commit()



@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if 'username' not in session:
        flash('请先登录。', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    if request.method == 'POST':
        post_content = request.form['post_content']
        if post_content:
            add_post(user_id, post_content)
            flash('帖子已发布！', 'success')
        else:
            flash('帖子内容不能为空。', 'danger')
    
    posts = get_all_posts()
    return render_template('forum.html', posts=posts)

@app.route('/reply/<int:post_id>', methods=['POST'])
def reply(post_id):
    if 'username' not in session:
        flash('请先登录。', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    reply_content = request.form['reply_content']
    if reply_content:
        add_reply(post_id, user_id, reply_content)
        flash('回复已发布！', 'success')
    else:
        flash('回复内容不能为空。', 'danger')
    
    return redirect(url_for('forum'))

# 在应用启动时初始化数据库
init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 从数据库中查询用户
        user = get_user(username, password)
        if user:
            session['username'] = username
            session['user_id'] = user[0]  # 存储用户ID以供后续使用
            flash('登录成功！', 'success')
            return redirect(url_for('about'))
        else:
            flash('用户名或密码错误，请重试。', 'danger')
    return render_template('login.html')

@app.route('/about')
def about():
    if 'username' not in session:
        flash('请先登录。', 'warning')
        return redirect(url_for('login'))
    
    return render_template('about.html', username=session['username'])

@app.route('/notebook', methods=['GET', 'POST'])
def notebook():
    if 'username' not in session:
        flash('请先登录。', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    if request.method == 'POST':
        content = request.form['content']
        if content:
            add_note(user_id, content)
            flash('笔记已添加！', 'success')
        else:
            flash('笔记内容不能为空。', 'danger')
    
    notes = get_notes(user_id)
    return render_template('notebook.html', notes=notes)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('您已注销。', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
