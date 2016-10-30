#!/usr/bin/python3


# def compile(source) :
#	if not source :
#		return ""
#	for part in separate(source) :
#		if not part :
#			return ""
#		leading = part[0]
#		if leading in keywords :
#			yield do[leading](part[1:])
#		else :
#			yield "movl $" + leading + ", %eax"

env = {"__root__":None}
paramCount = []
localCount = []

def compile(source) :
	object = ""
	while source :
#		print(source)
		leading = source[0]

		if leading == ";" :
			result, source = "\n", source[1:]
		elif leading == "if" :
			result, source = doIf(source[1:])
		elif leading == "while" :
			result, source = doWhile(source[1:])
		elif leading == "return" :
			result, source = doReturn(source[1:])
		elif leading == "call" :
			result, source = doCall(source[1:])
		elif leading == "function" :
			result, source = doFunction(source[1:])
		elif leading == "vars" :
			result, source = doVars(source[1:])
		elif leading == "for" :
			result, source = doFor(source[1:])
		elif leading.isnumeric() or (leading[0] == "-" and leading[1:].isnumeric()) :
			result, source = "movl $" + leading + ", %eax", source[1:]
		elif isIdentifier(leading) :
			result, source = get(leading), source[1:]
		
		object += "\n" + result + "\n"

	return object


def isIdentifier(token) :
	if token.isalnum() :
		return True
	token = token.replace("_", "")
	if token.isalnum() :
		return True
	if token[0] == "&" and token[1:].isalnum() :
		return True
	return False

def doReturn(stream) :
	end = findEnd(stream)
	return compile( stream[:end] ) + "\nleave\nret $" + str( (paramCount[-1]-2)*4), stream[end+1:]

def doVars(vars) :
	end = findEnd(vars)
	numVars = len( [addLocal(var) for var in vars[:end] if var != ","] )
	#printEnv()
	return "subl $" + str(numVars*4) + ", %esp", vars[end+1:]

def doCall(stream) :
	parts = []
	args = 1 if stream[0] != "(" else stream.index("(") # same...

	function = compile(stream[:args])
	stream = stream[args:]

	endArgs = findMatching(stream)
	params = stream[1:endArgs]

	if params :
		parts.append( doParams(params) )
	parts.append( function )
	parts.append( "\ncall *%eax" )

	return "\n".join(parts), stream[endArgs+1:]

def doFunction(stream) :

	name = stream[0]
	addLabel(stream[0])
	stream = stream[1:]

	newEnv()
	endParams = findMatching(stream)
	params = stream[1:endParams]
	[ addParam(param) for param in params if param != "," ]
	stream = stream[endParams+1:]

	endBody = findMatching(stream, "{", "}")
	body = stream[1:endBody]

	returned = name + ":\nenter $0, $0" + compile(body), stream[endBody+1:]
	endFunction()
	return returned

def newEnv() :
	global env, aparmCount, localCount
	env = {"__root__":env}
	paramCount.append(2)
	localCount.append(-1)

def endFunction() :
	global env, paramCount, localCount
	env = env["__root__"]
	paramCount.pop()
	localCount.pop()

def addParam(param) :
	global env, paramCount
	offset = str( paramCount[-1] * 4 )
	env[param] = "\nmovl " + offset + "(%ebp), %eax"
	env["&"+param] = "\nmovl %ebp, %eax\naddl $" + offset + ", %eax"
	paramCount[-1] += 1

def addLocal(local) :
	global env, localCount
	if local in env :
		return

	offset = str( localCount[-1] * 4 )
	env[local] = "\nmovl " + offset + "(%ebp), %eax"
	env["&"+local] = "\nmovl %ebp, %eax\naddl $" + offset + ", %eax"
	localCount[-1] -= 1

def addLabel(label) :
	global env
	env["&"+label] = env[label] = "\nmovl $" + label + ", %eax"

def get(var) :
	if var[:2] == "__" and var[-2:] == "__" :
		return "movl $" + var + ", %eax"

	current = env
	while var not in current :
		root = current["__root__"]
		if not root :
			return "movl $youSuck, %eax"
		current = root
	return current[var]


def doParams(params) :
	print(params)
	return "\n".join( (compile(param) + "\npushl %eax") for param in reversed(separate(params)) )

def separate(tokens, delim=",") :
	sep = []
	index = 0
	count = 0
	for i, token in enumerate(tokens) :
		if token == "(" :
			count += 1
		elif token == ")" :
			count -= 1
		elif count == 0 and token == "," :
			sep.append(tokens[index:i])
			index = i + 1
	sep.append(tokens[index:])

	return sep

whileCount = 0
def doWhile(stream) :
	parts = []
	condEnd = findMatching(stream)
	id = getID("while")

	parts.append( "start_while" + id + ":" )
	parts.append( compile( stream[1:condEnd] ) )
	parts.append( "cmp false, %eax\nje end_while" + id )
	stream = stream[condEnd+1:]

	endBlock = findMatching(stream, "{", "}")
	parts.append( compile(stream[1:endBlock]) )
	parts.append( "jmp start_while" + id + "\nend_while" + id + ":" )
	
	return "\n".join( parts ), stream[endBlock+1:]

forCount = 0
def doFor(stream) :
	parts = []
	iterVar = stream[0]
	addLocal(iterVar)
	id = getID("for")
#	parts.append("\nsubl $4, %esp")

	startBlock = stream.index("{")
	parts.append( compile(stream[2:startBlock]) )
	print(stream[2:startBlock])

	iterVarAddr = get(iterVar).split()[1][:-1]
	iterHead = "cmp $0, (%esp)\nje end_for" + id + "\npushl %ebp\nmovl (%ebp), %ebp" + "\nmovl %eax, " + iterVarAddr
	
	parts.append(iterHead)

	stream = stream[startBlock:]
	endBlock = findMatching(stream, "{", "}")
	parts.append( compile(stream[1:endBlock]) )

	iterFoot = "\npopl %ebp\nret\nend_for" + id + ":\naddl $4, %esp"
	parts.append(iterFoot)

	return "\n".join( parts ), stream[endBlock+1:]

ifCount = 0
def doIf(stream) :	# stream -> compiles, remainder
	parts = []
	condEnd = findMatching(stream)
	id = getID("if")

	parts.append( compile( stream[1:condEnd] ) ) 		#compile condition
	parts.append( "cmp false, %eax\nje else_clause" + id ) 	#check result
	stream = stream[condEnd+1:] 				#get rid of condition

	endTrue = findMatching(stream, "{", "}")		#find end of true block
	parts.append( compile(stream[1:endTrue]) )		#compile true block
	parts.append( "jmp end_if" + id + "\nelse_clause" + id + ":" )
	stream = stream[endTrue+1:]				#get rid of true block

	if stream and stream[0] == "else" :
		stream = stream[1:]
		endFalse = findMatching(stream, "{", "}")
		parts.append( compile(stream[1:endFalse]) )
		stream = stream[endFalse+1:]

	parts.append( "end_if" + id + ":" )

	return "\n".join(parts), stream

def doBlock(block) :
	return compile(block)

def getID(type) :
	global ifCount, whileCount, forCount
	if type == "if" :
		id = str(ifCount)
		ifCount += 1
	elif type == "while" :
		id = str(whileCount)
		whileCount += 1
	elif type == "for" :
		id = str(forCount)
		forCount += 1
	return id

		
def findEnd(stream, delim=";") :
	for i, token in enumerate(stream) :
		if token == delim :
			return i
 
def findMatching(stream, open="(", close=")") :
	count = 0
	for i, token in enumerate(stream) :
		if token == open :
			count += 1
		elif token == close :
			count -= 1
			if count == 0 :
				return i

def printEnv() :
	print("Environment : ")
	current = env
	tab = "\t"
	while current :
		for k, v in env.items() :
			if k != "__root__" :
				print(tab, k, ":", " / ".join(v.strip().split("\n")))
		current = current["__root__"]
		tab += "\t"
	
import sys
import subprocess
if __name__ == "__main__" :
	clargs = sys.argv

	program = '.include "std.s"\n.section .data\n.section .text\n'
	
	if  "-i" in clargs :
		program += compile( clargs[clargs.index("-i")+1].split() )
	elif "-f" in clargs :
		with open( clargs[clargs.index("-f")+1], "r" ) as file :
			program += compile( file.read().split() )

	program = "\n".join( line.strip() for line in program.split("\n") if line ) + "\n"
	if "-d" in clargs :
		print(program)

	filename = "compilerOutput0.s"
	if "-o" in clargs :
		filename = clargs[clargs.index("-o")+1]
		with open(filename, "w") as file :
			file.write(program)

		if "-r" in clargs :
			print("Result :")
			args = ["sudo", "./build", filename.replace(".s", "")]
			if "-a" in clargs :
				start = clargs.index("-a") + 2
				args.extend( clargs[ start: int(clargs[start-1])+start] )
			pgm = subprocess.Popen(args)
			pgm.wait()
		

