import time
import sys
import os
time.sleep(float(sys.argv[1]))
# os.system(sys.argv[:1])
cmdToRun = ''
arguments = sys.argv[2:]
for arg in arguments:
    cmdToRun += f' {arg}'
cmdToRun = cmdToRun[1:]
print(cmdToRun)