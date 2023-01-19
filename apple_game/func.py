import sys
import pyautogui as gui
from time import sleep
import winsound
from configure import resize_size
from torchvision import models
from torch import nn, cuda
import torch
from PIL import Image
import numpy as np
from functools import cmp_to_key

# 가로 세로 사과가 몇 개 있는지
row_cnt, col_cnt = 10, 17

class dot:
    def __init__(self, row, column):
        self.r = row
        self.c = column

class Loc:
    def __init__(self, depr, depc, desr, desc):
        self.depr = depr
        self.depc = depc
        self.desr = desr
        self.desc = desc

    def get_des(self):
        return self.desr, self.desc

    def get_dep(self):
        return self.depr, self.depc

class Circle:
    delta = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    move = 0

    def __init__(self, radius, center_r = 0, center_c = 0):
        self.center_r = center_r
        self.center_c = center_c
        self.radius = radius
        self.coord_r = self.center_r-radius
        self.coord_c = self.center_c
        self.stop = pow(2, radius+1)

    def __iter__(self):
        return self

    def __next__(self):
        if self.move < self.stop:
            cur_dir = self.delta[self.move//pow(2, self.radius-1)]
            self.coord_r += cur_dir[0]
            self.coord_c += cur_dir[1]
            self.move += 1
            return self.coord_r, self.coord_c
        else: raise StopIteration

def init_board_size(interval = 1):
    frequency = 1000  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

    sleep(interval)
    lt = gui.position()

    winsound.Beep(frequency, duration)

    sleep(interval)
    rb = gui.position()
    winsound.Beep(frequency, duration)

    return lt, rb

def get_sample_input(d):
    for r in range(1, row_cnt+1):
        d[r] = [0] + list(map(int, input().split()))

def init_fenwick(fenwick):
    for r in range(1, row_cnt+1):
        for c in range(1, col_cnt+1): fenwick[r][c] += fenwick[r][c-1]
        for c in range(col_cnt, 0, -1): fenwick[r][c] -= fenwick[r][c-(c&-c)]
        for c in range(1, col_cnt+1): fenwick[r][c] += fenwick[r-1][c]
    for r in range(row_cnt, 0, -1):
        for c in range(1, col_cnt+1): fenwick[r][c] -= fenwick[r-(r&-r)][c]

def trans(r1, c1, r2, c2):
    if r1 >= r2: r1, r2 = r2, r1
    if c1 >= c2: c1, c2 = c2, c1
    return dot(r1, c1), dot(r2, c2)

def prefix_sum(fenwick, r, c):
    ret = 0
    while r:
        tmpc = c
        while tmpc:
            ret += fenwick[r][tmpc]
            tmpc -= tmpc&-tmpc
        r -= r&-r
    return ret

def get_sum(fenwick, lt, rb):
    ret = prefix_sum(fenwick, rb.r, rb.c)
    ret -= prefix_sum(fenwick, rb.r, lt.c-1)
    ret -= prefix_sum(fenwick, lt.r-1, rb.c)
    ret += prefix_sum(fenwick, lt.r-1, lt.c-1)
    return ret

# d[r][c] = v
def update(d, fenwick, r, c, v):
    delta = v - d[r][c]
    d[r][c] = v
    while r <= row_cnt:
        tmpc = c
        while tmpc <= col_cnt:
            fenwick[r][tmpc] += delta
            tmpc += tmpc&-tmpc
        r += r&-r

def set_zero(d, fenwick, lt, rb):
    for r in range(lt.r, rb.r+1):
        for c in range(lt.c, rb.c+1):
            update(d, fenwick, r, c, 0)

def update_visited(not_visited, fenwick_visited, r, c, v):
    delta = v - not_visited[r][c]
    not_visited[r][c] = v
    while r <= row_cnt:
        tmpc = c
        while tmpc <= col_cnt:
            fenwick_visited[r][tmpc] += delta
            tmpc += tmpc&-tmpc
        r += r&-r

def check_visited(not_visited, fenwick_visited, lt, rb):
    for r in range(lt.r, rb.r+1):
        for c in range(lt.c, rb.c+1):
            update_visited(not_visited, fenwick_visited, r, c, 0)

def duration_setter(lt, rb):
    dist = abs(lt.r-rb.r) + abs(lt.c-rb.c)
    return 0.25+0.25*dist

def drag(lt, rb, loc, duration = 0.5):
    gui.moveTo(loc[lt.r][lt.c].get_dep())
    gui.dragTo(loc[rb.r][rb.c].get_des(), duration = duration_setter(lt, rb))

def get_region(left, top, width, height):
    # left, top, width, height
    return left-width/2, top-height/2, width, height

def collect(region):
    im = gui.screenshot(region=region).convert('L')
    im = im.resize(resize_size)
    im = np.asarray(im).reshape(1, 1, 28, 28)
    return im

def get_screen_input(d, loc, lt_screen, rb_screen):
    width = (rb_screen.x - lt_screen.x) / (col_cnt - 1)
    height = (rb_screen.y - lt_screen.y) / (row_cnt - 1)
    image = []
    for dtop in range(row_cnt):
        for dleft in range(col_cnt):
            left = lt_screen.x + width * dleft
            top = lt_screen.y + height * dtop
            region = get_region(left, top, width, height)
            loc[dtop+1][dleft+1] = Loc(region[0], region[1], region[0]+region[2], region[1]+region[3])
            image.append(collect(region))
    image = torch.from_numpy(np.asarray(image)).float()

    # image capture complete
    winsound.Beep(1000, 500)

    device = "cuda" if cuda.is_available() else "cpu"
    model = models.resnet18(pretrained=True)
    model.conv1 = nn.Conv2d(1, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
    model.fc = nn.Linear(model.fc.in_features, 9)
    model.to(device)

    best_checkpoint = torch.load("weight.pth", map_location=device)
    model.load_state_dict(best_checkpoint)

    model.to(device)
    model.eval()
    with torch.no_grad():
        for idx, X in enumerate(image):
            X = X.to(device)
            outputs = model(X)
            _, preds = torch.max(outputs, 1)
            # label은 정답 글자 - 1로 저장했었음
            q, r = divmod(idx, col_cnt)
            d[q+1][r+1] = int(preds) + 1

    for row in d: print(*row)

def custom_key(l, r):
    distl = abs(l[1]-row_cnt//2) + abs(l[2]-col_cnt//2)
    distr = abs(r[1]-row_cnt//2) + abs(r[2]-col_cnt//2)
    return distr - distl

def scheduler(d, schedule):
    tmp = []
    for r in range(1, row_cnt+1):
        for c in range(1, col_cnt+1):
            tmp.append((d[r][c], r, c))
    tmp.sort(reverse=True, key=cmp_to_key(custom_key))

    for _, r, c in tmp: schedule.append((r, c))