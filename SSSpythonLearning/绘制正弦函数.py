import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 创建绘图窗口
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)

# 初始的 x 和 y 数据
x = np.linspace(0, 2 * np.pi, 1000)
amplitude = 1
frequency = 1
phase = 0
y = amplitude * np.sin(frequency * x + phase)

# 绘制初始正弦波
line, = ax.plot(x, y)

# 设置图形标题和标签
ax.set_title('Interactive Sine Wave')
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
plt.grid(True)

# 创建滑块的布局，分别控制振幅、频率和相位
axcolor = 'lightgoldenrodyellow'
ax_amp = plt.axes([0.1, 0.2, 0.8, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)

# 创建滑块控件
slider_amp = Slider(ax_amp, 'Amplitude', 0.1, 5.0, valinit=amplitude)
slider_freq = Slider(ax_freq, 'Frequency', 0.1, 5.0, valinit=frequency)
slider_phase = Slider(ax_phase, 'Phase', 0.0, 2 * np.pi, valinit=phase)

# 更新正弦波函数的回调函数
def update(val):
    amp = slider_amp.val
    freq = slider_freq.val
    ph = slider_phase.val
    line.set_ydata(amp * np.sin(freq * x + ph))
    fig.canvas.draw_idle()

# 当滑块值变化时，调用 update 函数
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

# 显示图形
plt.show()