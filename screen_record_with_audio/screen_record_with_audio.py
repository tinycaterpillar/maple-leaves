from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import argparse
from subprocess import call
import pyautogui
import time
import winsound as sd
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--file_name', '-n', type=int)
args = parser.parse_args("")


# driver(selenium)
args.user_agent = ""  # https://www.whatismybrowser.com/detect/what-is-my-user-agent/

# record(ffmpeg)
args.file_name = int(sys.argv[1])
winsize = pyautogui.size()
# 노트북
if winsize == (1920, 1080):
    args.from_x = 1538
    args.from_y = 796
    args.offset_x = 1118
    args.offset_y = 560
    args.width = 774
    args.height = 440
    print("노트북")
# 학교
elif winsize == (3440, 1440):
    args.from_x = 2908
    args.from_y = 1074
    args.offset_x = 2582
    args.offset_y = 892
    args.width = 824
    args.height = 458
    print("학교")
args.show_mouse = False
args.show_region = True

options = Options()

# Preventing Detection
options.add_argument('user-agent=' + args.user_agent) #지정한 user-agent로 설정합니다.
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f"--window-position={args.offset_x},{args.offset_y}")
options.add_argument(f"--window-size={args.width},{args.height}")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get("https://code.plus/user/login")

# 로그인
driver.find_element(By.XPATH, '//*[@id="wrapper"]/section/div/div/div/form/fieldset/label[1]/input').send_keys("")
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("")
driver.find_element(By.XPATH, '//*[@id="wrapper"]/section/div/div/div/form/fieldset/button').click()

driver.get(f"https://code.plus/lecture/{args.file_name}")
driver.switch_to.frame(0)
driver.find_element(By.ID, 'pip-control-bar-button').click()
time.sleep(5)
pyautogui.moveTo(args.from_x, args.from_y, duration=0.5)
pyautogui.dragTo(args.offset_x, args.offset_y, duration=0.5)
time.sleep(5)

progressbar = driver.find_element(By.XPATH, '//*[@id="player"]/div[7]/div[8]/div[2]/div/div[1]/div/div[1]')
t = progressbar.get_attribute('aria-valuetext')
s = progressbar.get_attribute('aria-valuenow')
print(f"record from {s}")

args.duration = t.split('of')[-1].strip()

driver.find_element(By.XPATH, '//*[@id="player"]/div[7]/div[8]/div[1]/button').click()
cmd = f'ffmpeg -y -f dshow -t {args.duration} -i audio="virtual-audio-capturer" -rtbufsize 100M -f gdigrab -t {args.duration} -framerate 30 -offset_x {args.offset_x} -offset_y {args.offset_y} -s {args.width}x{args.height} -show_region {int(args.show_region)} -probesize 10M -draw_mouse {int(args.show_mouse)} -i desktop -c:v libx264 -r 30 -preset veryfast -tune zerolatency -crf 25 -pix_fmt yuv420p {args.file_name}.mp4' 
print(cmd)
call(cmd)

driver.quit()