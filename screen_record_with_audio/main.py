from subprocess import call
import time

# 강의 번호
lis = []
for i in range(517, 522): lis.append(i)

for num in lis:
    cmd = f"python screen_record_with_audio.py {num}"
    print("running:", cmd)
    call(cmd)