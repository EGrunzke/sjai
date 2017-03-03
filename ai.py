from enum import Enum
import pyautogui
import time
import random

# Live values
top_x = 1740
top_y = 134

# Dev values
# top_x = 257
# top_y = 361


class Tile(Enum):
    YELLOW = 1
    BLUE = 2
    PURPLE = 3
    GREEN = 4
    BLACK = 5
    RED = 6
    UNKNOWN = 9
    OOB = 10


class Board:
    def __init__(self):
        self.matrix = [[Tile.UNKNOWN for x in range(0, 8)] for y in range(0, 8)]
        self.matches = []
        self.raw = [[None for x in range(0, 8)] for y in range(0, 8)]

    def __str__(self):
        fmt = '\n'.join(['{}' for row in self.matrix])
        return fmt.format(*self.matrix)

    def scrape(self, x, y, width, height):
        pyautogui.moveTo(top_x-50, top_y-50)
        ss = pyautogui.screenshot(region=(x,y,width,height))

        for i in range(0, 8):
            for j in range(0, 8):
                px = ss.getpixel((j * 96 + 48, i * 96 + 48))
                self.raw[i][j] = px
                cc = closest_color(px)
                self.matrix[i][j] = cc

    def swap(self, i1, j1, i2, j2):
        """Swaps two tiles, if possible.  Returns True if swap was successful"""
        one = self.get_tile(i1,j1)
        two = self.get_tile(i2,j2)
        if one is Tile.OOB or two is Tile.OOB:
            return False

        self.matrix[i1][j1] = two
        self.matrix[i2][j2] = one
        return True

    def get_tile(self, i, j):
        if i < 0 or i > 7 or j < 0 or j > 7:
            return Tile.OOB
        else:
            return self.matrix[i][j]

    def find_moves(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.check_for_matches(i, j)
        print('MATCHES')
        print(self.matches)

    def check_for_matches(self, i, j):

        # First try the right-shift
        if self.swap(i, j, i, j + 1):
            ta = self.get_tile(i - 2, j)
            tb = self.get_tile(i - 2, j + 1)
            tc = self.get_tile(i - 1, j)
            td = self.get_tile(i - 1, j + 1)
            te = self.get_tile(i, j - 2)
            tf = self.get_tile(i, j - 1)
            tg = self.get_tile(i, j)
            th = self.get_tile(i, j + 1)
            ti = self.get_tile(i, j + 2)
            tj = self.get_tile(i, j + 3)
            tk = self.get_tile(i + 1, j - 2)
            tl = self.get_tile(i + 1, j - 1)
            tm = self.get_tile(i + 1, j)
            tn = self.get_tile(i + 1, j + 1)
            to = self.get_tile(i + 1, j + 2)
            tp = self.get_tile(i + 2, j)
            tq = self.get_tile(i + 2, j + 1)
            tr = self.get_tile(i + 3, j)
            if self.test_sequences(
                    (te, tf, tg),
                    (tf, tg, th),
                    (tg, th, ti),
                    (th, ti, tj),
                    (ta, tc, tg),
                    (tc, tg, tm),
                    (tg, tm, tp),
                    (tb, td, th),
                    (td, th, tn),
                    (th, tn, tq)):
                right_shift = (i, j, i, j + 1)
                self.matches.append(right_shift)

            # Regardless of outcome, swap back
            self.swap(i, j, i, j + 1)

        # Then try the down-shift
        if self.swap(i, j, i + 1, j):
            ta = self.get_tile(i - 2, j)
            tb = self.get_tile(i - 2, j + 1)
            tc = self.get_tile(i - 1, j)
            td = self.get_tile(i - 1, j + 1)
            te = self.get_tile(i, j - 2)
            tf = self.get_tile(i, j - 1)
            tg = self.get_tile(i, j)
            th = self.get_tile(i, j + 1)
            ti = self.get_tile(i, j + 2)
            tj = self.get_tile(i, j + 3)
            tk = self.get_tile(i + 1, j - 2)
            tl = self.get_tile(i + 1, j - 1)
            tm = self.get_tile(i + 1, j)
            tn = self.get_tile(i + 1, j + 1)
            to = self.get_tile(i + 1, j + 2)
            tp = self.get_tile(i + 2, j)
            tq = self.get_tile(i + 2, j + 1)
            tr = self.get_tile(i + 3, j)
            if self.test_sequences(
                    (te, tf, tg),
                    (tf, tg, th),
                    (tg, th, ti),
                    (ta, tc, tg),
                    (tc, tg, tm),
                    (tg, tm, tp),
                    (tm, tp, tr),
                    (tk, tl, tm),
                    (tl, tm, tn),
                    (tm, tn, to)):
                self.matches.append((i, j, i + 1, j))

            # Regardless of outcome, swap back
            self.swap(i, j, i + 1, j)

    def test_sequences(self, *args):
        for seq in args:
            if seq[0] == seq[1] and seq[1] == seq[2]:
                return True
        return False


colors = {
    Tile.YELLOW: (161, 130, 39),
    Tile.BLUE: (98, 222, 221),
    Tile.PURPLE: (112, 49, 117),
    Tile.GREEN: (162, 161, 107),
    Tile.BLACK: (167, 167, 167),
    Tile.RED: (223, 48, 11)
}


def color_distance(a, b):
    red_diff = abs(a[0] - b[0])
    green_diff = abs(a[1] - b[1])
    blue_diff = abs(a[2] - b[2])
    return red_diff + green_diff + blue_diff


def closest_color(pixel):
    best = 1000
    co = Tile.UNKNOWN
    for key, val in colors.items():
        diff = color_distance(pixel, val)
        if diff < best:
            best = diff
            co = key
    return co


def find_moves(board):
    pass


def main_loop():
    enabled = False
    # Main loop
    while True:
        if pyautogui.position() == (2559, 0):
            enabled = not enabled
            if not enabled:
                print("PAUSING FOR 5 SECONDS")
                pyautogui.moveTo(1280,720)
                time.sleep(5)
        print(enabled)

        if enabled:
            board = Board()
            board.scrape(top_x, top_y, 768, 768)
            board.find_moves()
            random.shuffle(board.matches)
            for ix in range(0, min(5, len(board.matches))):
                match = board.matches[ix]
                pyautogui.click(x=top_x + 48 + match[1] * 96, y=top_y + 48 + match[0] * 96)
                time.sleep(.15)
                pyautogui.click(x=top_x + 48 + match[3] * 96, y=top_y + 48 + match[2] * 96)
                time.sleep(.15)
        time.sleep(1)


def quick_grab():
    b = Board()
    b.scrape(top_x, top_y, 768, 768)
    print(b)
    f = '\n'.join(['{}' for row in b.raw])
    print(f.format(*b.raw))

main_loop()
