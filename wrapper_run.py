import subprocess
import os
import time
import run
for i in range(31):
	p = subprocess.Popen(['python', 'run.py'])
	time.sleep(4)
	p.terminate()


	
