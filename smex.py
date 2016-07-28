# import logging



class NextState(Exception):
	pass

class SM(object):

	def go(stateName,*args, **kwargs):
		raise NextState (SM._fn(stateName),args,kwargs)

	def __init__(this):
		this.states = {}
		this.activeState = None
		this._errorState = None
		# this.debug = False

	def _fn(stateName):
		""" Returns the callable name OR if stateName is a string just return it """
		nextState = None
		if hasattr(stateName, '__call__'): # check if this is a callable 
			nextState = stateName.__name__
		else:
			nextState = stateName	
		return nextState

	def errorState(this,stateName):
		this._errorState = SM._fn(stateName)

	# def preRun(this,oldstate,newstate):
	def preRun(this):	
		""" Overwrite me """
		pass

	# def postRun(this,oldstate,newstate):
	def postRun(this):
		""" Overwrite me """
		pass

	def add(this,stateFunc):
		""" 
			Add state functions to the state machine
			then they're callable with their 
			function name like so:
			
			def state1():
				print("Hello from state1")
			
			sm = SM()
			sm.add(state1)
			sm.go("state1")  # or  sm.go(state1)
		"""
		this.states[stateFunc.__name__] = stateFunc

	def start(this,stateName):
		""" starts the state machine main loop """
		print("Starting at:", stateName)
		this.activeState = stateName
		while True:
			try:
				this.preRun()
				this.states[this.activeState]()
				print("State [%s] did not go to another state, so exitting" % this.activeState)
				break				
			except NextState as exp:
				this.postRun()			
				print ("Going to state:",exp.args[0])
				this.activeState = exp.args[0]
				continue
			except Exception as exp:
				# A state has trown an error withouth 
				# catching it, if the state machine 
				# has an default error state
				# we switch to it
				if this._errorState:
					print ("")
					print ("==================")
					print ("| ERROR IN STATE |")
					print ("==================")
					print (exp)
					print ("Going to default Error State:",this._errorState)
					this.activeState = this._errorState
					continue
				else:
					raise exp					

						
