# (APP:p:is)	e	s		h
# is		e	(Arg:len h:s)	(h ++ [THU,p,e])
def appState() :
	global code, env, stack, heap, pc, run, ret
	pointer = len(heap)
	heap.extend( (THU, code[pc], env) )
	stack.append( pointer )
	stack.append( ARG )
	pc += 1

# (LAM:is)	e	s	h
# *(len h)	_	s	(h ++ [CLO, is, e])
def lamState() :
	global env, heap, pc
	pointer = len(heap)
	heap.extend( (CLO, pc, env) )
	cloState(pointer)

# (Ind:n:is)	(...:*p)	s	h
# *p		_		s	h
def indState() :
	global code, env, stack, heap, pc, run, ret
	pointer = get(code[pc])
	heapStates[heap[pointer]](pointer)

# (APPI:n:is)	(...:*p)	s		h
# is		(...:*p)	(ARG:*p:s)	h
def appIState() :
	global code, env, stack, heap, pc, run, ret
	pointer = get(code[pc])
	stack.append( pointer )
	stack.append( ARG )
	pc += 1

# (APPC:pc:is)	e	s		h
# is		e	(ARG:*p:s)	[...p->CLO:pc:e]
def appCState() :
	global code, env, stack, heap, pc, run, ret
	pointer = len(heap)
	heap.extend( (CLO, code[pc]+1, env) )
	stack.append( pointer )
	stack.append( ARG )
	pc += 1
	
# (FOR:is)	[*p...]		s		[...p->THU:pc:e']
# pc		e'		(CON:*q:s)	[...p->...q->CLO:is:e]
def forState() :
	global code, env, stack, heap, pc, run, ret
	pointer = len(heap)
	thunk = env[0]
	heap.extend( (THU, pc, env) )
	stack.append( pointer )
	stack.append( CON )
	heapStates[heap[thunk]](thunk)

def caseState() :
	global code, env, stack, heap, pc, run, ret
	pointer = get(code[pc])
	table = code[pc+1]
	tag = heap[pointer+1]
	pc = static[table+tag]

#caseState: #%esi -> program counter
#movl (%esi), %ecx
#call __get__
#movl 4(%esi), %ebx
#addl 4(%eax), %ebx
#jmp *%ebx

#__get__: #index in %ecx
#movl %ebp, %eax
#start_get:
#test %ecx, %ecx
#jz end_get
#	movl (%eax), %eax
#	jmp end_get
#end_get
#movl 4(%eax), %eax
#ret



# *p	_	s	[...VOID]
# ERROR	-> Circular evaluation
def voidState(pointer) :
	global code, env, stack, heap, pc, run, ret
	raise Exception("Should not evaluate voided object!", heap[pointer:pointer+3])

# *p	_	s		[...THU:pc:e]
# pc	e	(UPD:*p:s)	[...VOID]
def thuState(pointer) :
	global code, env, stack, heap, pc, run, ret
	pc = heap[pointer+1]
	env = heap[pointer+2]
	heap[pointer] = VOID
	stack.append(pointer)
	stack.append( UPD )

# *p	_	[]	[...CLO:pc:e]
# HALT 	->	(CLO,pc,e)
def cloState(pointer) :
	global code, env, stack, heap, pc, run, ret
	if stack :
		stackStates[stack.pop()](pointer)
	else :
		run = False
		ret = heap[pointer:pointer+3]


# *p	_	(UPD:q:s)	[...p->CLO:pc:e...q->VOID]
# *p	_	s		[...p->CLO:pc:e...q->CLO:pc:e]
def updState(pointer) :
	global code, env, stack, heap, pc, run, ret
	updPointer = stack.pop()
	if heap[updPointer] == VOID :
		heap[updPointer:updPointer+3] = heap[pointer:pointer+3]
		cloState(pointer)
	else :
		raise Exception("Cannot update live object!")

# *p	_	(ARG:q:s)	[...p->CLO:pc:e]
# pc	(q:e)	s		[...]
def argState(pointer) :
	global code, env, stack, heap, pc, run, ret
	pc = heap[pointer+1]
	env = heap[pointer+2]
	env = (stack.pop(), env)

# *p	_	(CON:cl:s)	[...cl->CLO:pc:e]
# *cl	_	s		[...]
def conState(pointer) :
	global code, env, stack, heap, pc, run, ret
	closure = stack.pop()
	thuState(closure)


# E !! n
def get(index) :
	global env
	local = env
	for n in range(index) :
		local = local[1]
	return local[0]


APP, LAM, IND, APPI, APPC, FOR	= 0, 1, 2, 3, 4, 5
UPD, ARG, CON			= 0, 1, 2
THU, CLO, VOID			= 0, 1, 2


codeStates	= [appState, lamState, indState, appIState, appCState, forState]
stackStates	= [updState, argState, conState]
heapStates	= [thuState, cloState, voidState]


# A thread
code	= None
env	= None
stack	= None
heap	= None

pc	= 0
run	= True
ret	= None
steps	= 0

def evaluate(parts) :
	global code, env, stack, heap
	code	= parts["code"]
	env	= []
	stack	= parts.get("stack", [])
	heap	= parts.get("heap", [])
	
	return execute()

def execute() :
	global run, ret
	while run :
		step()
	return ret

def step() :
	global code, pc, steps
	state = code[pc]
	pc += 1
	steps += 1
	codeStates[state]()


def show(pc) :
	global code
	tag = code[pc]
	if tag == LAM :
		return "\\" + show(pc+1)
	elif tag == APP :
		return "(" + show(pc+2) + " " + show(code[pc+1]) + ")"
	elif tag == IND :
		return str(code[pc+1])
	elif tag == APPI :
		return "(" + show(pc+2) + " " + str(code[pc+1]) + ")"
	elif tag == APPC :
		return "(" + show(pc+2) + " " + show(code[pc+1]) + ")"
	elif tag == FOR :
		return "!" + show(pc+1)
	else :
		raise Exception("Oh noes!")

def lambdaToN(closure) :
	value = 0
	while show(closure[1]) != '\\0' :
		value += 1
		pointer = closure[2][0]
		closure = heap[pointer:pointer+3]
	return value

#	show :: [Instruction] -> String
#	show (Lam : is) = '\\' : show is
#	show (APP l:is) = '(' : show is ++ ' ' : show l ++ ")"
#	show (Ind n:is) = show n

import lexer
import parser
import unsugarer
import assembler
import generator

if __name__ == "__main__" :

	langLexer = lexer.load("lang.lex")
	langParser = parser.load("lang.par")
	langUnser = unsugarer.load("lang.uns")
	assm = assembler.load("lang.lasm")

	with open("lambda.lang") as file :
		code = file.read()

	lexed = langLexer.lex(code)
	parsed = langParser.parse(lexed)
	unsuged = langUnser.unsugar(parsed)
	gened = generator.generate(unsuged)

	print(gened)
	assmed = assm.assemble(gened)

	print(assmed, "\n")
	interpreted = evaluate(assmed)
	
	address = interpreted[1]
	print("------------------------------------ Done\n")
#	print(code)
	print("Program : ", show(0), "\n")
#	print("CLOS : ", interpreted)
	print(lambdaToN(interpreted))
	print("\\" + show(address))
	print(len(heap), " memory blocks")
	print(steps, " steps")
