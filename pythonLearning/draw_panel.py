import json
import turtle
import math

## 创建turtle画布
screen = turtle.Screen()
screen.title("Draw Pamel")
screen.setworldcoordinates(-360, -1.5, 360, 1.5) # 设置画布的坐标范围

## 创建画笔
pen=turtle.Turtle() # 创建一个Turtle对象，命名为pen
pen.speed(1) # 设置绘制速度（1是最慢，10是最快，0是无延迟的最快)
pen.width(2) # 设置画笔的宽度
pen.color("red") # 设置画笔的颜色


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

draw_axes()
## 开始主循环
screen.mainloop()