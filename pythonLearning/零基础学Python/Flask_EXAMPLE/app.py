import flask
from flask import request, render_template_string

app = flask.Flask(__name__)

@app.route('/')
def home():
    return 'Hello World! Hello Flask! 这是我的第一个Flask应用'

@app.route('/about')
def about():
    return f"这里是我的一个页面"

@app.route('/user/<name>')
def user(name):
    return f"你好, {name}"

## 上下二选一

# 首页，显示表单
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 从表单获取用户输入
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        return f"您输入的内容是:<br>姓名: {name}<br>年龄: {age}<br>电子邮件: {email}"
 
    # 显示表单
    return render_template_string('''
        <form method="post">
            <table>
                <tr>
                    <td><label for="name">姓名:</label></td>
                    <td><input type="text" id="name" name="name" required></td>
                </tr>
                <tr>
                    <td><label for="age">年龄:</label></td>
                    <td><input type="number" id="age" name="age" required></td>
                </tr>
                <tr>
                    <td><label for="email">电子邮件:</label></td>
                    <td><input type="email" id="email" name="email" required></td>
                </tr>
                <tr>
                    <td colspan="2"><input type="submit" value="提交"></td>
                </tr>
            </table>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')