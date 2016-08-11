""" 
	This is an example of a full finite state machine utilizing smex.
	It will drink and piss and sleep for you.
"""

from smex import SM
import time 
import sys
import random

def drinking(what="beer"):
	print ("DRINKING", what)
	print(this.pissLevel)
	if what == "beer":
		this.pissLevel +=  random.randint(4,10)
	if what == "SCHNAPS":
		this.pissLevel +=  random.randint(2,4)
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
	print("zzZZZzzzZZZzzzZZZ")
	time.sleep(5.2)
	SM.go(drinking,what="SCHNAPS")


def errorState():
	print("the pissbot is broken, we go sleeping to recover from the shock : ) ")
	time.sleep(1)
	SM.go(sleeping)

pissbot = SM()
pissbot.debug(True)
def trans(oldState,newState):
	""" Here we could do something on state change. """ 
	print(oldState,"->",newState)
pissbot.transition(trans)
pissbot.pissLevel = 10
pissbot.add(drinking)
pissbot.add(pissing)
pissbot.add(sleeping)
pissbot.add(errorState)
pissbot.errorState(errorState)
pissbot.start(drinking,what="beer")