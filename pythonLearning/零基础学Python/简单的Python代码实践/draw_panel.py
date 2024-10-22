import json
import turtle
import math

## 创建turtle画布
screen = turtle.Screen()
screen.title("Draw Pamel")
screen.setworldcoordinates(-360, -1.5, 360, 1.5) # 设置画布的坐标范围

## 创建画笔
pen=turtle.Turtle() # 创建一个Turtle对象，命名为pen
pen.speed(6) # 设置绘制速度（1是最慢，10是最快，0是无延迟的最快)
pen.width(2) # 设置画笔的宽度
pen.color("red") # 设置画笔的颜色

## 存储绘制的动作
actions = []

## 函数：记录绘制动作
def start_drawing(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    actions.append(("penup", x, y))
    actions.append("pendown")
def draw(x, y):
    pen.goto(x, y)
    actions.append(("goto", x, y))

## 函数：绘制坐标轴
def draw_axes():
    pen.penup()
    pen.goto(-360, 0)
    pen.pendown()
    pen.goto(360, 0)
    pen.penup()
    pen.goto(0, -1.5)
    pen.pendown()
    pen.goto(0, 1.5)
    pen.penup()

## 函数：绘制正弦函数
def draw_function():
    pen.penup()
    x = -360
    x_radius = math.radians(x)
    y = math.sin(x_radius)
    pen.goto(x, y)
    pen.pendown()
    while x <= 360:
        x += 1
        x_radius = math.radians(x)
        y = math.sin(x_radius)
        pen.goto(x, y)

## 函数：清除画布
def clear_canvas():
    pen.clear()
    actions.clear()

## 函数：退出程序
def exit_program():
    screen.bye()
    exit()

## 函数：保存绘制到文件
def save_drawing():
    with open("pythonLearning/零基础学Python/drawing.json", "w") as file:
        json.dump(actions, file)
    print("绘图已经保存到drawing.json")

## 函数：从文件加载并重现绘制
def load_drawing():
    pen.clear()
    try:
        with open("pythonLearning/零基础学Python/drawing.json", "r") as file:
            loaded_actions = json.load(file)
        for action in loaded_actions:
            if action[0] == "penup":
                pen.penup()
                pen.goto(action[1], action[2])
            elif action[0] == "pendown":
                pen.pendown()
            elif action[0] == "goto":
                pen.goto(action[1], action[2])
    except FileNotFoundError:
        print("没有找到drawing.json文件")

## 绑定鼠标事件到turtle画布
pen.ondrag(draw) # 鼠标拖动时绘制
screen.onclick(start_drawing) # 鼠标点击时开始绘制

## 添加保存和加载功能
screen.listen()
screen.onkey(save_drawing, "s") # 按下s键保存绘制
screen.onkey(load_drawing, "l") # 按下l键加载绘制
## 绑定快捷键到turtle画布
screen.onkey(draw_axes, "a") # 按下a键绘制坐标轴
screen.onkey(draw_function, "f") # 按下f键绘制函数
screen.onkey(clear_canvas, "z") # 按下z键清除画布
screen.onkey(exit_program, "e") # 按下e键退出程序

## 开始主循环
screen.mainloop()