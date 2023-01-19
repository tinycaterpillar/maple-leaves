import func
import sys
import os.path
from copy import deepcopy
import win32api
if os.path.isfile("sample.txt"): sys.stdin = open('sample.txt')
if os.path.isfile("cur_data.txt"): sys.stdout = open('cur_data.txt', 'w')

def look_around(cr, cc, ub):
    for r in range(1, func.row_cnt + func.col_cnt):
        # if all of r is bigger than 10, flag = True
        flag = True
        for nr, nc in func.Circle(radius=r, center_r=cr, center_c=cc):
            if nr <= 0 or nr > func.row_cnt or nc <= 0 or nc > func.col_cnt: continue
            lt, rb = func.trans(nr, nc, cr, cc)

            apple_cnt = func.get_sum(fenwick_visited, lt=lt, rb=rb)
            cur_sum = func.get_sum(fenwick, lt=lt, rb=rb)
            if apple_cnt > ub: continue
            if cur_sum < 10: flag = False
            elif cur_sum == 10:
                flag = False
                func.set_zero(d, fenwick, lt=lt, rb=rb)
                func.check_visited(not_visited, fenwick_visited, lt, rb)
                func.drag(lt, rb, loc)
                print(lt.r, lt.c)
                print(rb.r, rb.c)
                print("apple_cnt", apple_cnt)
                print("ub", ub)
                # for i in d: print(*i)
                print("===" * 10)
                return True
        if flag: return False
    return False

# lt : 좌측 상단(left top) 사과의 중심 좌표
# rb : 우측 하단 사과의 중심 좌표
lt_screen, rb_screen = func.init_board_size(2)

loc = [[0]*(func.col_cnt+1) for _ in range(func.row_cnt+1)]
d = [[0]*(func.col_cnt+1) for _ in range(func.row_cnt+1)]
# func.get_sample_input(d)
func.get_screen_input(d, loc, lt_screen, rb_screen)

schedule = []
func.scheduler(d, schedule)

fenwick = deepcopy(d)
func.init_fenwick(fenwick)
not_visited = [[1]*(func.col_cnt+1) for _ in range(func.row_cnt+1)]
fenwick_visited = [[1]*(func.col_cnt+1) for _ in range(func.row_cnt+1)]
for r in range(func.row_cnt): fenwick_visited[r][0] = 0
for c in range(func.col_cnt): fenwick_visited[0][c] = 0
func.init_fenwick(fenwick_visited)

ub = 2
while ub < 10:
    endloop = True
    for cr, cc in schedule:
        # exit program to hold ESC button
        if win32api.GetKeyState(0x1B) < 0:
            print("Terminated by user")
            sys.exit()

        if not not_visited[cr][cc]: continue
        if look_around(cr, cc, ub):
            endloop = False
            break
    if endloop: ub += 1