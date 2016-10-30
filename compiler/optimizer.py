#!/usr/bin/python3

import lexer
import parser
import unsugarer
import translator
import flattener

import copy

level = 0
showSteps = False
reportResult = True

test = ("caseexp", [("cons", 0), [("lambda", [("index", "0")])] ])
# data Exp = Ind Int | Lam Exp | App Exp Exp | Case Exp [Int] | Cons Int | Tup [Int]

def optimize(tree) :
	if level > 0:
		finalState = stateInit( ("field", tree, 0) )
		tree = finalState[0]
		if reportResult :
			report(*finalState)
	return tree

def report(tree, env, heap) :
	print("RESULT : " + str(numSteps) + " steps\n")
	print(flattener.flatten(tree))
	for e in summarize(env, heap) :
		print()
		for k, v in e.items() :
			print(k, ":", v)

subs = []
def translate(tree) :
	type = tree[0]
	if type == "index" :
		return "GET", + str(tree[1]) + "\n"
	elif type == "lambda" :
		return "LAM\n" + translate(tree[1])
	elif type == "apply" :
		var = fresh()
		if tree[2][0] == "index" :
			return "APPi " + str(tree[2][1]) + "\n" + translate(tree[1])
		subs.append( var + ":\n" + translate(tree[2]) )
		return "APP " + var + "\n" + translate(tree[1])
	else :
		raise Exception("Illegal Expression!", tree)

# data Bytecode = Ind n | App x | Lam
# type Instructions = [Bytecode]

# "bytecode" translation :
#	subs.append( "main :\n" + translate(tree) )
#	print( "\n".join( reversed(subs) ) )



fr = 0
def fresh() :
	global fr
	var = "v" + str(fr)
	fr = fr + 1
	return var

def summarize(env, heap) :
	return sumEnv(env), sumHeap(heap)

def sumEnv(env, n=0) :
	defs = {}
	while env :
		defs[n] = "*" + str(env[0][1])
		n = n+1
		env = env[1]
	return defs

def sumHeap(heap) :
	defs = {}
	for i, (t, (e, v)) in enumerate(heap) :
		v = sumEnv(v)
		e = flattener.flatten(e)
		if t == "thunk" :
			e = "\\()." + e
		defs[i] = (e, v)
	return defs

def cons(*xxs) :
	return xxs

def get(n, xs) :
	for n in range(n) :
		xs = xs[1]
	return xs[0]

def choose(n, alts) :
	return alts[n]

def toTuple(ls) :
	if ls :
		return toTuple(ls[1]) + [ls[0]]
	return []

# Data types used :
#	data Exp = Ind Int | Lam Exp | App Exp Exp

# 	data Data = Bits Int | Reference Exp | Pointer Int
# 	type Env = [Data]

#	type Closure a = (a, Env)
#	type Case = Exp
#	type Cases = [Case]
# 	data Continuation = Argument Data | Update Int | Cases (Closure Cases)
# 	type Stack = [Continuation]

#	data Thunk = Void | Thunk (Closure Exp) | Evaled (Closure Exp)
# 	Heap = [Reference]

# 	State = (Data, Env, Stack, Heap)

# Driver :
# 	transition :: State -> State


# \E | (f x) | N
# 4 instruction machine, 3 registers : code + env + cont | heap
#	(f a)	env	cont		heap
#	f	env	*:cont		heap++(a,env)

#	\E	env	*:cont		heap
#	E	*:env	cont		heap

#	\E	env	#:cont		heap
#	\E	env	cont		heap[#]=(\E,env)

#	N	[..N:*]	  cont		heap
#	*	_	  cont		heap
#	heap[*]	heap[**]  #:cont	heap

# ... | {t} | (t,vs)
# + Data Constructors (really just tuples)
#	case e of alt*	[]	cont			heap
#	e		[]	(alt*, []):cont		heap

#	{t}		[vs]	cont			heap
#	(t,vs)		_	cont			heap

#	(,)		[vs]	cont			heap 	-- Not now...
#	(vs)		_	cont			heap

#	(t,vs)		_	(alt*, []):cont		heap
#	alts[t]		[]	(t,vs):cont		heap
#	alt[t]		[*]	cont			heap++(t,vs)

#	(t,vs)		_	#:cont			heap
#	(t,vs)		_	cont			heap[#]=(t,vs)

# N	(0,  n)
# \E 	(1, exp)
# (f a)	(2, f, a)
# (e[])	(3, e, [])

# lambda, apply, index ++ closure, thunk, pointer, update
# ... ++ bits, builtin (?)

# (->) : Const = \x.e, Select = (f x)
# (X)  : Cont  = (,), Select = force e as a b c in e

# Heap  :: Closure Lam Env | Thunk Body Env | VOID | Tuple [Pointer n]
# Prog  :: Lam Body | App f x | Ind n | Tuple [Pointer n] | CONS | DONE
# Stack :: Update n | Pointer n | ABORT

current = None
env = ()
cont = [("abort", [])]
heap = []

def stateInit(input) :
	global current
	current = input
	num = 0
	while True :
		if showSteps :
			print("Step " + str(num), current, env, cont, heap, "\n", sep="\n")
		num += 1

		type = current[0]
		if type == "index" :
			stateIndex()
		elif type == "apply" :
			stateApply()
		elif type == "lambda" :
			stateLambda()
		elif type == "construct" :
			stateConstruct()
		elif type == "field" :
			stateField()
		elif type == "tuple" :
			stateTuple()
		elif type == "done" :
			global numSteps
			numSteps = num
			return current[1]
		else :
			raise Exception("Illegal State!", current, env)

# code  :: %esi
# env   :: %ebp
# stack :: %esp


def stateField() : # ( "field", exp, n)
	global current, env, cont, heap
	cont.append( ( "pick", current[2] ) )
	current = current[1]

def stateIndex() :
	global current, env, cont, heap
	current, env = get( current[1], env ), None	
	statePointer()

def statePointer() :
	global current, env, cont, heap
	index = current[1]
	(objtype, objparts) = heap[index]
	if objtype == "thunk" :
		stateThunk(index, objparts)
	elif objtype == "closure" :
		stateClosure(objparts)
	elif objtype == "tuple" :
		stateHTuple(objparts)
	elif objtype == "VOID" :
		stateVoidAccess()

def stateHTuple(fields) :
	global current, env
	current, env = ("tuple", fields), ()

def stateClosure(objparts) :
	global current, env, cont, heap
	current, env = objparts

def stateThunk(index, objparts) :
	global current, env, cont, heap
	current, env = objparts
	cont.append( ("update", index) )
	heap[index] = ("VOID", None)	

def stateVoidAccess() :
	raise Exception("Circular definition!")

def stateApply() :
	global current, env, cont
	x = current[2]
	if x[0] == "index" :
		stateAIndex(x[1])
	elif x[0] == "lambda" :
		stateALambda(x)
	elif x[0] == "apply" :
		stateAApply(x)
	elif x[0] == "construct" :
		stateAApply(x)
	current = current[1]

def stateAIndex(index) :
	cont.append( get(index, env) )

def stateALambda(x) :
	cont.append( ("pointer", len(heap)) )
	heap.append( ("closure", (x, env))  )

def stateAApply(x) :
	cont.append( ("pointer", len(heap)) )
	heap.append( ("thunk", (x, env))  )

def stateTuple() :
	global current, env, cont, heap
	cctype, ccparts = cont.pop()
	if cctype == "update" :
		stateTUpdate(ccparts)
	elif cctype == "pick" :
		statePick(ccparts)
	elif cctype == "abort" :
		stateAbort()

def statePick(n) :
	global current, env, cont, heap
	current, env = current[1][n], ()
	statePointer()

def stateTUpdate(index) :
	global current, env, cont, heap
	heap[index] = current

def stateLambda() :
	global current, env, cont, heap
	(cctype, ccparts) = cont.pop()
	if cctype == "update" :
		stateLUpdate(ccparts)
	elif cctype == "pointer" :
		stateArgument(current[1], ccparts)
	elif cctype == "abort" :
		stateAbort()

def stateAbort() :
	global current, env, heap
	current = ("done", [current, env, heap])

def stateLUpdate(index) :
	global current, env, cont, heap
	heap[index] = ("closure", (current, env))

def stateArgument(sub, index) :
	global current, env
	current, env = sub, cons(("pointer", index), env)

def stateConstruct() :
	global current, env
	current, env = ("tuple", toTuple(env)), ()



globals = {}

def load(filename) :
	global globals
#	with open(filename, "r") as file :
#		globals = {name:tree for name, tree in [ processline(line) for line in file if line.strip() ] }
#		globals = {name:optimize(tree) for name, tree in globals.items()}

def processline(line) :
	name = line.split()[0]
	translator.globals.append(name)

	code = " ".join(line.split()[2:])
	return (name, unsugarer.unsugar(parser.parse(lexer.lex(code))))
