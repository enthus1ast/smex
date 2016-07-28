from smex import SM
import time
import random
def  scan ():
	# hier mach ich was
	# if True:
	print("\tHello from state scan")
	time.sleep(1)
	if random.randint(0,1):
		print("\tFound targets!")
		SM.go(ddos)
	else:
		print ("\tNothing :/")
		SM.go(idle)

def ddos():
	# hier was anders
	print("\tHello from state ddos :) ")
	time.sleep(1)
	# raise KeyError ("HALLO")
	SM.go(idle)

def idle():
	print ("\tIDLEING")
	time.sleep(5)
	SM.go(scan)

# def sendStatus()


sm = SM()
# sm.preRun = preRun
# sm.postRun = postRun
sm.add(ddos)
sm.add(scan)
sm.add(idle)
sm.errorState("scan")	
sm.start("scan")
