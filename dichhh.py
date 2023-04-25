import numpy as np
from numpy import absolute as nabs
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def collision(x1, vx1, x2, vx2, radius, mass1, mass2):
    """Аргументы функции:
    x1, vx1 - координата и скорость 1-ой частицы
    x2, vx2 - координата и скорость 2-ой частицы
    radius, mass1, mass2 - радиус частиц и их массы
    """

    # Расчет расстояния между центрами частиц
    r12 = np.sqrt((x1 - x2) ** 2)

    # Проверка условия на столкновение: расстояние
    # должно быть меньше 2-х радиусов
    if r12 <= 2 * radius:
        # Пересчет  скорости первой частицы
        VX1 = vx1 * (mass1 - mass2) / (mass1 + mass2) \
              + 2 * mass2 * vx2 / (mass1 + mass2)

        # Пересчет скорости второй частицы
        VX2 = vx2 * (mass2 - mass1) / (mass1 + mass2) \
              + 2 * mass1 * vx1 / (mass1 + mass2)

    else:
        # Eсли условие столкновнеия не выполнено,
        # то скорости частиц не пересчитываются
        VX1, VX2 = vx1, vx2

    return VX1, VX2


def move_func(s, t):
    x1, v_x1, x2, v_x2 = s

    dx1dt = v_x1
    dv_x1dt = 1 - 5 * np.sin(t)

    dx2dt = v_x2
    dv_x2dt = 0

    return dx1dt, dv_x1dt, dx2dt, dv_x2dt


# Парамаетры и условия тестового примера
mass1 = 1
mass2 = 1
radius = 0.5

x10 = 0
x20 = 250
v10 = 1
v20 = - 1

# Массивы для записи итоговых координат объектов
x1 = [x10]
x2 = [x20]

# Разбиение общего времени моделирования на интервалы
T = 100
N = 1000
tau = np.linspace(0, T, N)

# Цикл для расчета столкновений
for k in range(N - 1):
    t = [tau[k], tau[k + 1]]
    s0 = x10, v10, x20, v20

    sol = odeint(move_func, s0, t)

    x10 = sol[1, 0]
    x20 = sol[1, 2]
    x1.append(x10)
    x2.append(x20)

    v10 = sol[1, 1]
    v20 = sol[1, 3]
    res = collision(x10, v10, x20, v20, radius, mass1, mass2)
    v10 = res[0]
    v20 = res[1]

# Графический вывод
fig, ax = plt.subplots()

ball_1, = plt.plot([], [], 'o', color='r', ms=25)
ball_2, = plt.plot([], [], 'o', color='r', ms=25)
ax.set_xlim(-500, 500)
ax.set_ylim(-1, 1)


def animate(i):
    ball_1.set_data((x1[i], 0))
    ball_2.set_data((x2[i], 0))


ani = FuncAnimation(fig, animate, frames=N, interval=30)
ani.save('collision.gif')
