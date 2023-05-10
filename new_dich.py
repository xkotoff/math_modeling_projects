import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def collision(x1, vx1, x2, vx2, 
              y1, vy1, y2, vy2,
              radius, mass1, mass2):
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
        VX1 = 0
        VY1 = -1

        # Пересчет скорости второй частицы
        VX2 = 0
        VY2 = -1
        print('hello collision')

    else:
        # Eсли условие столкновнеия не выполнено,
        # то скорости частиц не пересчитываются
        VX1, VX2 = vx1, vx2
        VY1, VY2 = vy1, vy2

    return VX1, VY1, VX2, VY2


def move_func(s, t):
    (x1, v_x1, y1, v_y1,
     x2, v_x2, y2, v_y2) = s

    dx1dt = v_x1
    dv_x1dt = 1 - 5 * np.sin(t)
    dy1dt = v_y1
    dv_y1dt = 0

    dx2dt = v_x2
    dv_x2dt = 0
    dy2dt = v_y2
    dv_y2dt = 0

    return (dx1dt, dv_x1dt, dy1dt, dv_y1dt,
            dx2dt, dv_x2dt, dy2dt, dv_y2dt)


# Парамаетры и условия тестового примера
mass1 = 1
mass2 = 1
radius = 20

x10 = 5000
vx10 = 0.04
y10 = 7800
vy10 = 0

x20 = 10000
vx20 = 10
y20 = 7800
vy20 = 0

# Массивы для записи итоговых координат объектов
x1 = [x10]
y1 = [y10]
x2 = [x20]
y2 = [y20]

# Разбиение общего времени моделирования на интервалы
T = 100
N = 1000
tau = np.linspace(0, T, N)

# Цикл для расчета столкновений
for k in range(N - 1):
    t = [tau[k], tau[k + 1]]
    s0 = x10, vx10, y10, vy10, x20, vx20, y20, vy20

    sol = odeint(move_func, s0, t)

    x10 = sol[1, 0]
    y10 = sol[1, 2]
    x20 = sol[1, 4]
    y20 = sol[1, 6]
    x1.append(x10)
    y1.append(y10)
    x2.append(x20)
    y2.append(y20)

    vx10 = sol[1, 1]
    if tau[k] > 50:
     #   vx20 = -5
        print('START')
    else:
        vx20 = -10
    res = collision(x10, vx10, x20, vx20, y10, vy10, y20, vy20, radius, mass1, mass2)
    vx10 = res[0]
    vy10 = res[1]
    vx20 = res[2]
    vy20 = res[3]

# Графический вывод
fig, ax = plt.subplots()

ball_1, = plt.plot([], [], 'o', color='r', ms=25)
ball_2, = plt.plot([], [], '<', color='r', ms=5)
ax.set_xlim(3000, 11299)
ax.set_ylim(1, 8000)


def animate(i):
    ball_1.set_data((x1[i], y1[i]))
    ball_2.set_data((x2[i], y2[i]))


ani = FuncAnimation(fig, animate, frames=N, interval=30)
ani.save('collision.gif')
