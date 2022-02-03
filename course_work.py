from PIL import Image
from PIL import ImageDraw
from math import sqrt


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


# обратно, единичный диск a + bi --> пиксели (c, d)
def reverse(z):
    return round(z.real * R_x + R_x), round(-z.imag * R_y + R_y)


def reflection(z, v):
    answer = (-2 * v + z * (1 + (abs(v))**2)) / (2 * v.conjugate() * z - (1 + (abs(v))**2))
    return complex(round(answer.real, 4), round(answer.imag, 4))


z1 = complex_coordinates(complex(pol[0][0], pol[0][1]))
z2 = complex_coordinates(complex(pol[1][0], pol[1][1]))
z3 = complex_coordinates(complex(pol[2][0], pol[2][1]))


# уравнение прямой диска пуанкаре, которое проходит через 2 точки z1 и z2, зависит от параметра а
# эта функция ищет параметр а
def find_a(z1, z2):
    spisok = []
    for i in range(0, width):
        for j in range(0, height):
            a = complex_coordinates(complex(i, j))
            s1 = a * (z2 - z1) + a.conjugate() * (abs(z2) ** 2 * z1.conjugate() - abs(z1) ** 2 * z2.conjugate())
            s2 = abs(a) ** 2 * (abs(z1) ** 2 - abs(z2) ** 2) - z2 * z1.conjugate() + z1 * z2.conjugate()
            if abs(s1 + s2) < 1e-3:
                spisok.append([a, s1 + s2])
    spisok.sort(key=lambda x: abs(x[1]))
    return spisok[0][0]


# лежит ли точка на прямой, которая проходит через точки z1 и z2 (a = find_a(z1, z2))
def the_point_is_on_the_line(z, z1, a):
    m1 = (z1 - a.conjugate() * abs(z1)**2) * (z.conjugate() - a)
    m2 = (z - a.conjugate() * abs(z)**2) * (z1.conjugate() - a)
    if abs(m1 - m2) < 1e-3 / 2:
        #draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                     #fill='blue', outline='blue')
        return 'the line contains the point'
    return 'no'


def the_point_is_on_the_line_segment(z):
    if the_point_is_on_the_line(z, z1, a_12) == 'the line contains the point':
        if z.real > z1.real:
            draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                         fill='blue', outline='blue')
            return [z, z3]
        #elif z.real < z2.real:
        #    draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
        #                 fill='green', outline='green')
    elif the_point_is_on_the_line(z, z2, a_23) == 'the line contains the point':
        if z.imag > z2.imag:
            draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                         fill='blue', outline='blue')
            return [z, z1]
        #elif z.imag < z3.imag:
        #    draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
        #                 fill='green', outline='green')
    elif the_point_is_on_the_line(z, z3, a_31) == 'the line contains the point':
        if z.imag < z3.imag:
            draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                         fill='blue', outline='blue')
            return [z, z2]
        #elif z.imag > z1.imag:
        #    draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
        #                 fill='green', outline='green')
    return [0, 0]


def left_billiards(z, z_i, count):
    a_i = reflection(z, z_i)
    draw.ellipse((reverse(a_i)[0] - 2, reverse(a_i)[1] - 2, reverse(a_i)[0] + 2, reverse(a_i)[1] + 2),
                 fill='black', outline='black')
    if count - 1 != 0:
        if z_i == z1:
            z_i = z3
        elif z_i == z2:
            # точка может попасть только в два из трёх сегментов
            z_i = z1
        elif z_i == z3:
            z_i = z2
        return left_billiards(a_i, z_i, count - 1)
    else:
        return


def draw_triangle(z):
    if the_point_is_on_the_line(z, z1, a_12) == 'the line contains the point' and z1.real > z.real > z2.real:
        draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                     fill='red', outline='red')
    elif the_point_is_on_the_line(z, z2, a_23) == 'the line contains the point' and z2.imag > z.imag > z3.imag:
        draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                     fill='red', outline='red')
    elif the_point_is_on_the_line(z, z3, a_31) == 'the line contains the point' and z3.imag < z.imag < z1.imag:
        draw.ellipse((reverse(z)[0] - 2, reverse(z)[1] - 2, reverse(z)[0] + 2, reverse(z)[1] + 2),
                     fill='red', outline='red')
    return


a_12 = find_a(z1, z2)
a_23 = find_a(z2, z3)
a_31 = find_a(z3, z1)
for i in range(0, width):
    for j in range(0, height):
        z = complex_coordinates(complex(i, j))
        if abs(z) < 1:
            a, b = the_point_is_on_the_line_segment(z)
            if [a, b] != [0, 0]:
                left_billiards(a, b, 2)
        if abs(z) <= max(abs(z1), abs(z2), abs(z3)):
            draw_triangle(z)
print(z1, z2, z3)


draw.polygon(pol, fill='red')
image.save("image15.png", "PNG")
image.show()
