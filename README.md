smex
=====
Smex is a simple state machine.

Usage:	

	from smex import SM
	
	def go1():
		SM.go(go2)
	def go2():
		SM.go(go1)
	sm = SM()
	sm.add(go1)
	sm.add(go2)
	sm.start("go1")


OR



	""" 
		This is an example of a simple machine 
		A state is a normal function.
		The state has to call 
		SM.go("otherState")
		somewhere
		
	"""
	
	def  scan ():
		# hier mach ich was
		# if True:
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
		# raise KeyError ("HALLO")
		SM.go(idle)

	def idle():
		print ("\tIDLEING")
		time.sleep(5)
		SM.go(scan)

	sm = SM() 
	sm.debug(True)
	sm.add(flying) # we add the functions
	sm.add(scan) # to our state
	sm.add(idle) # machine.
	sm.errorState("scan") # when a function is not catching all Exceptions we go to this state
	sm.start("scan") # we start the maschine at the state scan


Get more help/examples by looking at the source code of
smex.py , pissbot.py , smtests.py
