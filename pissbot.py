from smex import SM
import time 
import sys
import random

def drinking():
	print(this.pissLevel)
	# exit()

	# global pissLevel
	this.pissLevel +=  random.randint(1,10)
	time.sleep(0.2)
	if this.pissLevel >= 10:
		SM.go(pissing)
	else:
		SM.go(drinking)

def pissing():
	if this.pissLevel > 10:
		sys.stdout.write("PISSING ")
		sys.stdout.flush()
		sys.stdout.write("\n")
		time.sleep(0.5)
		this.pissLevel = 0 #

	SM.go(sleeping)

def sleeping():
	time.sleep(5.2)
	SM.go(drinking)


pissbot = SM()
pissbot.pissLevel = 10
pissbot.add(drinking)
pissbot.add(pissing)
pissbot.add(sleeping)
pissbot.start(drinking)