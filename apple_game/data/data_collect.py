import configure
import func
import pyautogui
from configure import resize_size
from configure import data_cnt
import winsound

data_cnt = configure.data_cnt
def get_region(left, top, width, height):
    # left, top, width, height
    return left-width/2, top-height/2, width, height

def collect(region):
    global data_cnt

    num_image = pyautogui.screenshot(region=region).convert('L')
    num_image = num_image.resize(resize_size)

    # label_serial
    num_image.save(f"{1}_{data_cnt}.png")
    data_cnt += 1

# lt : 좌측 상단(left top) 사과의 중심 좌표, rb : 우측 하단 사과의 중심 좌표
lt, rb = func.init_board_size()

# 가로 세로 사과가 몇 개 있는지
row_cnt, col_cnt = 10, 17

# rb.x = left = rb.column, rb.y = top = rb.row
width = (rb.x - lt.x)/(col_cnt - 1)
height = (rb.y - lt.y)/(row_cnt - 1)
for dtop in range(row_cnt):
    for dleft in range(col_cnt):
        left = lt.x + width*dleft
        top = lt.y + height*dtop
        collect(get_region(left, top, width, height))

configure.data_cnt = data_cnt
winsound.Beep(1000, 500)
