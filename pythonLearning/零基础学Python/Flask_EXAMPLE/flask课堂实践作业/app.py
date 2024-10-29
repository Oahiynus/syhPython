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
