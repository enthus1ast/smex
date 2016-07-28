""" 
	A simple state machine
	Please have a look at the "./examples" directory.

	Import like so:
		from smex import SM
"""

class NextState(Exception):
	""" 
		We raise this to break out of the current state. DO NOT CATCH THIS! 
	"""
	pass

class NewStateInfo(object):
	""" 
		We use this to tell the next state how to run
		we can spezify arguments and positional arguments

	"""

	def __init__(this, stateName,args=[],kwargs={}):
			this.nextState = SM._fn(stateName)
			this.args = args 
			this.kwargs = kwargs 
		

class SM(object):
	"""
		smex Simple State machine
		usage:
			
			from smex import SM
			
			def go1():
				SM.go(go2)

			def go2():
				SM.go(go1)

			sm = SM()
			sm.add(go1)
			sm.add(go2)
			sm.start("go1")
		More examples:
			have a look at the "./examples" dir

		More Info:
			all states are called from the state machine object.
			So in every state "this" points to the state machine object.
			So you can store and retreive data from state to state by using this.mydata = 123
		More Info:
			one yould also append args and kwargs to the state by:
			SM.go("state",some,args,some="more", args=":)")
	"""
	def go(stateName,*args, **kwargs):
		""" 
			Use SM.go(statename) to switch between states
			You have to call the class methode go()  NOT the objects

			You can provide arguments with go("statename",some,arguments="foo") # TODO

			go() is breaking out of the current executed state by throwing an NextState
			exception, this gets catched by the state machine, then it starts the next state.
		"""
		newStateInfo = NewStateInfo(stateName,args,kwargs)
		raise NextState (newStateInfo)

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
		""" 
			Overwrite me 
			This gets called before the new state is executed.
			if you want to do something before a state is run, overwrite this in the state 
			machine level.
		"""
		pass

	# def postRun(this,oldstate,newstate):
	def postRun(this):
		""" 
			Overwrite me 
			This gets called after a state was executed.
			if you want to do something after a state has run.		
		"""
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
		stateFunc.__globals__.update(vars())
		this.states[stateFunc.__name__] = stateFunc

	def start(this,stateName,*args, **kwargs):
		""" 
			starts the state machine main loop,
			begin with the state "stateName"
		"""
		this.newStateInfo = NewStateInfo(SM._fn ( stateName ),args, kwargs)
		print("Starting at:", this.newStateInfo.nextState)
		this.activeState = this.newStateInfo.nextState
		
		while True:
			try:			
				this.preRun()
				this.states[this.activeState](*this.newStateInfo.args, **this.newStateInfo.kwargs )
				print("State [%s] did not go to another state, so exitting" % this.activeState)
				break				
			except NextState as exp:
				this.newStateInfo = exp.args[0]

				this.postRun()			
				print ("Going to state:",this.newStateInfo.nextState)
				this.activeState = this.newStateInfo.nextState
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

						
