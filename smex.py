""" 
	A simple state machine
	For complete examples please have a look at the:
			pissbot.py
		or
			smtests.py
		file.

	Import like so:
		from smex import SM
"""
import logging
import sys

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
		smex  - Simple state Machine EXtendet -
		[ https://github.com/enthus1ast/smex ]
		
		usage
		=====
			
			from smex import SM
			
			def go1():
				SM.go(go2)

			def go2():
				SM.go(go1)

			sm = SM()
			sm.add(go1)
			sm.add(go2)
			sm.start("go1")

		For more examples have a look at:
				pissbot.py
			or
				smtests.py
			file.

		Arguments to states
		===================

			one could also append args and kwargs to the state by:
			SM.go("state",args,some="more")

		Transitions
		===========
			you can react on a state change:
				sm = SM()
				def trans(oldState,newState):
					print(oldState,"->",newState)
				sm.transition(trans)		

		Share data
		==========
			every state can acces the sm object through `this`:
				this.mydata = 123
			mydata is visible from every state
	"""
	def go(stateName,*args, **kwargs):
		""" 
			Use SM.go(statename) to switch between states
			You have to call the class methode go() NOT the objects

			You can provide arguments with SM.go("statename",some,arguments="foo")

			go() is breaking out of the current executed state by throwing an NextState
			exception, this gets catched by the state machine, then it starts the next state.
			
			So catching ALL Exceptions will not work:
				def stateFoo():
					try:
						# do something 
						SM.go("otherState")
					except Exception:
						# i will break the state machine :/
		"""
		newStateInfo = NewStateInfo(stateName,args,kwargs)
		raise NextState (newStateInfo)

	def __init__(this):
		this.log = logging.getLogger("smex")
		this.log.addHandler(logging.StreamHandler(sys.stdout))
		this.states = {}
		this.activeState = None
		this.oldState = None # this is the state before the current active state
		this._errorState = None # a default state where the prog can recover from an error etc.
		this.transitionFunc = lambda src,dst: None # pre run dummy function
		# this.debug = False

	def _fn(stateName):
		""" Returns the callable name OR if stateName is a string just return it """
		nextState = None
		if hasattr(stateName, '__call__'): # check if this is a callable, we test if this obj CAN quack :)
			nextState = stateName.__name__
		else:
			nextState = stateName	
		return nextState

	def debug(this,debugEnabled):
		""" sm.debug(True) to get more status msgs """
		if debugEnabled: 
			this.log.level = logging.INFO

	def errorState(this,stateName):
		""" specify the state that is swiched to if an exception is not catched by a state """
		this._errorState = SM._fn(stateName)

	def _transition(this,src,dst):
		this.transitionFunc(src,dst)

	def transition(this,func):	

		""" 
			This gets called before the new state is executed.
			if you want to do something before a state is running ( while "transisting")


			def myTransitionFun():
				print("i'm called before the state is executed")

			sm = SM()
			sm.transition(myTransitionFun)
			....

		"""
		if hasattr(func, '__call__'): # check if this is a callable, we test if this obj CAN quack :)
			this.transitionFunc = func
		else:
			raise ValueError ("func should be a callable!")
		
	# def postRun(this,oldstate,newstate):
	# def postRun(this,src=None,dst=None):
	# 	""" 
	# 		Overwrite me 
	# 		This gets called after a state was executed.
	# 		if you want to do something after a state has run.	
	# 		same usage as preRun	
	# 	"""
	# 	pass

	def add(this,stateFunc):
		""" 
			Add state functions to the state machine
			then they're callable with their 
			function name like so:
			
			def state1():
				print("Hello from state1")
			
			sm = SM()
			sm.add(state1)

			#sm.go(state1) # SM.go ist smart enough to get the name out of a callable
			sm.go("state1")    
		"""
		stateFunc.__globals__.update({"this":this}) # we make this available inside the states, le magic... 
		this.states[stateFunc.__name__] = stateFunc

	def start(this,stateName,*args, **kwargs):
		""" 
			starts the state machine main loop,
			begin with the state "stateName"
		"""
		this.newStateInfo = NewStateInfo(SM._fn ( stateName ),args, kwargs)
		this.log.info("Starting at: [%s]" % this.newStateInfo.nextState)
		this.activeState = this.newStateInfo.nextState
		
		while True:
			try:
				this.transitionFunc(this.oldState,this.activeState) 
			except Exception:
				print("Error in transition function [%s] -> [%s]" % (this.oldState,this.activeState))
				raise

			try:			
				this.states[this.activeState](*this.newStateInfo.args, **this.newStateInfo.kwargs )
				this.log.error("State [%s] did not go to another state, so exitting" % this.activeState)
				break				
			except NextState as exp:
				this.newStateInfo = exp.args[0]
				# this.postRun() # todo..			
				this.log.info ("Going to: [%s]" % this.newStateInfo.nextState)
				this.oldState = this.activeState
				this.activeState = this.newStateInfo.nextState
				continue
			except Exception as exp:
				# A state has thrown an error withouth 
				# catching it, if the state machine 
				# has an default error state
				# we switch to it
				if this._errorState:
					this.log.error ("")
					this.log.error ("==================")
					this.log.error ("| ERROR IN STATE | -> %s" % this.newStateInfo.nextState )
					this.log.error ("==================")
					this.log.error (exp)
					this.log.error ("")
					this.log.error ("Going to default Error State: %s" % this._errorState)
					this.activeState = this._errorState
					this.newStateInfo = NewStateInfo(SM._fn ( this.errorState ),[], {}) # atm the error state is not accepting parameters
					continue
				else:
					raise					

					
if __name__ == '__main__':
	sm = SM()

	def u():
	    input("hallo")

	def trans(a,b):
		print(a,"->",b)
	sm.transition(trans)
	sm.add(u)	
	sm.start(u)