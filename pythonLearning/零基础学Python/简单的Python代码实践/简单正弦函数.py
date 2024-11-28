# 我想要使用 matplotlib 库绘制一个正弦函数的图像（示例：y = sin(x)，x 取值范围为 -2π 到 2π）
import matplotlib.pyplot as plt
import numpy as np

# x 的取值范围 (-2π, 2π)
x = np.linspace(-2 * np.pi, 2 * np.pi, 400)

# y = sin(x)
y = np.sin(x)

#绘制图像
plt.plot(x, y)

#设置.title(), legend()等各种设置
plt.title('sine function')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()