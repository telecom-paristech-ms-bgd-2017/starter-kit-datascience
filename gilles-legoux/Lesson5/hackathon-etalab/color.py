#!/usr/bin/env python3

# standard library imports
import math

# related third party imports
import numpy


def get_colors(dict_dep_val):
    values = dict_dep_val.values()
    _min = min(values)
    _max = max(values)
    colors = get_grid_colors()
    n_colors = len(colors)
    d = {}
    for key, val in dict_dep_val.items():
        d[str(key)] = colors[get_index_color(_min, _max, n_colors, val)]
    print('var colors = ', end='')
    print(d)


def get_index_color(_min, _max, n_colors, val):
    assert _min <= val <= _max
    alpha = (_max - _min)/n_colors
    index = math.floor((val - _min)/alpha)
    return index if index < n_colors else n_colors - 1


def get_rgb(r, g, b, alpha):
    return 'rgba({},{},{},{})'.format(r, g, b, alpha)


def get_hex(r, g, b):
    return '#{}{}{}'.format(get_color(r), get_color(g), get_color(b))


def get_color(n):
    assert 0 <= n <= 0xff, n
    return '{:02x}'.format(n)


def get_hexa_color_keep_blue(n):
    if 3*0xff >= n >= 2*0xff:
        r, g, b = n - 2*0xff, 0xff, 0xff
    elif 2*0xff > n >= 0xff:
        r, g, b = 0, n - 0xff, 0xff
    else:
        r, g, b = 0, 0, n
    return get_hex(r, g, b)


def get_grid_colors(m=100, n=3*0xff - 115):
    return [get_hexa_color_keep_blue(x) for x in range(m, n)]


def get_grid_html(m=100, n=3*0xff - 115):
    print('<!DOCTYPE html>')
    print('<html>')
    print('<body>')
    print(len(range(m, n)), 'colors')
    print('<table>')
    print('<tboby>')
    get_content_table(m=100, n=3*0xff - 115)
    print('</tboby>')
    print('</table>')
    print('</body>')
    print('</html>')


def get_content_table(colorize=get_hexa_color_keep_blue, m=100, n=3*0xff - 115, p=10, step=1):
    k = 0
    for i in range(m, n, step):
        k += 1
        if k == 1:
            print('<tr>')
        print(get_cell(colorize(i)))
        if k == p:
            print('</tr>')
            k = 0


def get_cell(color):
    return '<td style="background-color:{};height:20px;width:20px"></td>'.format(color)


if __name__ == "__main__":
    get_grid_html()
