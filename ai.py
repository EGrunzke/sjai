import pyautogui

# Live values
top_x = 1740
top_y = 134

# Dev values
top_x = 257
top_y = 361

colors = {
    'Y': (202, 163, 48),
    'B': (89, 217, 216),
    'P': (83, 7, 103),
    'G': (79, 111, 50),
    'K': (180, 180, 181),
    'R': (212, 46, 12)
}


def scrape_board():
    ss = pyautogui.screenshot(region=(top_x, top_y, 768, 768))

    matrix = []
    for y in range(0, 8):
        row = []
        for x in range(0, 8):
            px = ss.getpixel((x*96+48,y*96+48))
            cc = closest_color(px)
            row.append(cc)
        print(row)
        matrix.append(row)
    return matrix


def color_distance(a, b):
    red_diff = abs(a[0] - b[0])
    green_diff = abs(a[1] - b[1])
    blue_diff = abs(a[2] - b[2])
    return red_diff + green_diff + blue_diff


def closest_color(pixel):
    best = 1000
    co = ''
    for key, val in colors.items():
        diff = color_distance(pixel, val)
        if diff < best:
            best = diff
            co = key
    return co


def find_moves(board):
    pass

print(scrape_board()[0][1])