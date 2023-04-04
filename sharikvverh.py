import numpy as np
import random
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Определяем переменную величину и количество кадров
frames = 200
t = np.linspace(0, 5, frames)

# Определяем функцию для системы диф. уравнений
def move_func(z, t):
    x, v_x, y, v_y = z
    dxdt = v_x
    dv_xdt = 0
    dydt = v_y
    dv_ydt = (( q1*g*v)/m)-g
    return dxdt, dv_xdt, dydt, dv_ydt
# Определяем начальные значения и параметры
g = 9.8
q1= 1.2754
q = 0.173
r = 0.04
V = 4/3*np.pi*r
m = q*V+1.75
alpha = 80 * np.pi / 180
v = 2
u = 5
x0 = 0
v_x0 = 0
y0 = 0
v_y0 = 0

z0 = x0, v_x0, y0, v_y0
# Решаем систему диф. уравнений
sol = odeint(move_func, z0, t)
def solve_func(i, key):
    if key == 'point':
        x = sol[i, 0]
        y = sol[i, 2]
    else:
        x = sol[:i, 0]
        y = sol[:i, 2]
    return x, y

# Строим решение в виде графика и анимируем
fig, ax = plt.subplots()

ball, = plt.plot([], [], 'o', color='blue')
ball_line, = plt.plot([], [], '-', color='blue')
def animate(i):
    ball.set_data(solve_func(i, 'point'))
    ball_line.set_data(solve_func(i, 'line'))

ani = FuncAnimation(fig,
                    animate,
                    frames=frames,
                    interval=30)

edge = 100
ax.set_xlim(-3, edge)
ax.set_ylim(0, edge )

ani.save("pic58.gif")
