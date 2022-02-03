from PIL import Image
from PIL import ImageDraw
from math import sqrt

# нарисовать точки, которые после первой итерации переходит в луч, на котором бильярд не определён

# image6 -- образ точек при отражении относительно точки z1, которые лежат в первом сегменте
# (выше lin1 и правее lin2)

width = 1001
height = 1001
R_x, R_y = int(width / 2), int(height / 2)
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)
center = complex(R_x, R_y)
r = 50
pol = [(R_x+r, R_y), (R_x - r/2, R_y - sqrt(3) * r / 2), (R_x - r/2, R_y + sqrt(3) * r / 2)]
draw.rectangle((0, 0, width - 1, height - 1), fill='white', outline='white')
draw.ellipse((0, 0, width - 1, height - 1), fill=(255, 255, 0), outline='yellow')
draw.polygon(pol, fill='red')


def complex_coordinates(z):
    return complex((z.real - R_x) / R_x, -(z.imag - R_y) / R_y)


# обратно, единичный диск a+bi --> пиксели (c, d)
def reverse(z):
    return round(z.real * R_x + R_x), round(-z.imag * R_y + R_y)


def reflection(z, v):
    answer = (-2 * v + z * (1 + (abs(v))**2)) / (2 * v.conjugate() * z - (1 + (abs(v))**2))
    return complex(round(answer.real, 4), round(answer.imag, 4))


# прямая вида Ах+Ву+С=0, функция выдаёт [A, B, C]
def line(a, b):
    x1, y1 = a.real, a.imag
    x2, y2 = b.real, b.imag
    if x1 != x2:
        k, b = round((y2 - y1) / (x2 - x1), 3), round((y1 * x2 - y2 * x1) / (x2 - x1), 3)
        return [k, -1, b]
    elif x1 == x2:
        x = -x1
        return [1, 0, x]


# проверить местоположение точки z относительно прямой Ах+Ву+С = 0, параметры хранятся в списке s
# a, b, z -- в комплексных координатах, то есть a.imag, a.real \in [0, 1]
def line_z(z, s):
    if s[1] == -1:
        y_x = round(s[0] * z.real + s[2], 3)
        # если z.imag > y(x), то точка z находится ниже прямой. точки z.imag == y(x) не рассматриваем
        if round(z.imag, 3) > y_x:
            return True
        elif round(z.imag, 3) < y_x:
            return False
        else:
            return 'the line contains the point'
    # вертикальная прямая
    elif s[1] == 0:
        # если z.real < x1, то точка z находится слева от прямой
        if round(z.real, 3) < -s[2] and abs(round(z.real, 3) + s[2]) > 1e-3:
            return True
        elif round(z.real, 3) > -s[2] and abs(round(z.real, 3) + s[2]) > 1e-3:
            return False
        else:
            return 'the line contains the point'


def the_point_is_on_the_line_segment(z, z0):
    if (line_z(z0, lin2) == 'the line contains the point' and z0.imag > z2.imag) or \
            (line_z(z0, lin1) == 'the line contains the point' and z0.imag < z1.imag) or \
            (line_z(z0, lin3) == 'the line contains the point' and z0.imag < z3.imag):
        draw.ellipse((reverse(z0)[0] - 2, reverse(z0)[1] - 2, reverse(z0)[0] + 2, reverse(z0)[1] + 2),
                     fill='blue', outline='blue')
        draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                     fill='black', outline='black')
    return


def right_billiards(start, a_n, z_i, count):
    a_i = reflection(a_n, z_i)
    the_point_is_on_the_line_segment(start, a_i)
    if count - 1 != 0:
        if z_i == z1:
            z_i = z2
        elif z_i == z2:
            z_i = z3
        elif z_i == z3:
            z_i = z1
        return right_billiards(start, a_i, z_i, count - 1)
    else:
        return


z1 = complex_coordinates(complex(pol[0][0], pol[0][1]))
z2 = complex_coordinates(complex(pol[1][0], pol[1][1]))
z3 = complex_coordinates(complex(pol[2][0], pol[2][1]))
lin1, lin2, lin3 = line(z1, z2), line(z2, z3), line(z1, z3)
x = (z2.conjugate() - z1.conjugate() + z1 - z2) / (z1.conjugate() * z1 - z2.conjugate() * z2)
a_conj = complex(round(x.real, 4), round(x.imag, 4))
a = a_conj.conjugate()
for i in range(0, width):
    for j in range(0, height):
        z = complex_coordinates(complex(i, j))
        if abs(z) < 1:
            if line_z(z, lin1) and not(line_z(z, lin2)):
                right_billiards(z, z, z2, 15)
            if line_z(z, lin2) and line_z(z, lin3):
                right_billiards(z, z, z3, 15)
            if not(line_z(z, lin3)) and not(line_z(z, lin1)):
                right_billiards(z, z, z1, 15)
image.save("image10.png", "PNG")
image.show()
