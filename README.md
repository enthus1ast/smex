smex
=====
Smex is a simple state machine.



Usage:	
```python
from smex import SM

def go1():
	SM.go(go2)
def go2():
	SM.go(go1)
sm = SM()
sm.add(go1)
sm.add(go2)
sm.start("go1")
```

OR
```python
""" 
	This is an example of a simple machine 
	A state is a normal function.
	The state has to call 
	SM.go("otherState")
	somewhere
	
"""

def  scan ():
	# hier mach ich was
	print("\tHello from state scan")
	time.sleep(1)
	if random.randint(0,1):
		print("\tFound targets!")
		SM.go(flying)
	else:
		print ("\tNothing :/")
		SM.go(idle)

def flying():
	# hier was anders
	print("\tHello from state flying :) ")
	time.sleep(1)
	SM.go(idle)

def idle():
	print ("\tIDLEING")
	time.sleep(5)
	SM.go(scan)

sm = SM() 
sm.debug(True) # print the state changes
sm.add(flying) # we add the functions
sm.add(scan) # to our state
sm.add(idle) # machine.
sm.errorState("scan") # when a function is not catching all Exceptions we go to this state
sm.start("scan") # we start the maschine at the state scan
```

OR
```python
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
	print("zzZZZzzzZZZzzzZZZ")
	time.sleep(5.2)
	SM.go(drinking,what="SCHNAPS")

def errorState():
	print("the pissbot is broken, we go sleeping to recover from the shock : ) ")
	time.sleep(1)
	SM.go(sleeping)

pissbot = SM()
pissbot.debug(True)
pissbot.pissLevel = 10
pissbot.add(drinking)
pissbot.add(pissing)
pissbot.add(sleeping)
pissbot.add(errorState)
pissbot.errorState("errorState")
pissbot.start(drinking,what="beer")
```
Get more help/examples by looking at the source code of
smex.py , pissbot.py , smtests.py