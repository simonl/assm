#!/usr/bin/python3

import lexer
import parser
import translator
import optimizer
import unsugarer
import simplifier
import flattener


import sys
import subprocess

lexemes     = False
parseTree   = False
unsugTree   = False
optimTree   = False
translation = False
flattened   = False

Verbose    = False
Optimize   = False
Generate   = True

def compile(source) :
	vprint("Lexing ... \n")
	tokens 		= lexer.lex		(   source  )
	show(lexemes, "Token List : \n", tokens)

	vprint("Parsing ... \n")
	tree 		= parser.parse		(   tokens  )
	showTree(parseTree, "Parse Tree : \n", tree)

	vprint("Unsugaring ... \n")
	tree = unsugarer.unsugar   (  tree   )
	showTree(unsugTree, "Unsugared Tree : \n", tree)

	tree = simplifier.simplify(tree)

	if Optimize :
		vprint("Optimizing ... " + str(optimizer.level) + "\n")
		tree = optimizer.optimize  (  tree   )
		showTree(optimTree, "Optimized Tree : \n", tree)

	if flattened :
		vprint("Flattening ... \n")
		show(flattened, "Flattened Tree : \n", flattener.flatten(tree))

	if Generate :
		vprint("Translating ... \n")
		translator	. addfunc		( tree )
		show(translation, "Generated Assembly ... \n", translator.getresult() )

	return translator.getresult()


def showTree(doit, msg, tree) :
	if doit :
		print(msg)
		parser.printf(tree)
		print()

def show(doit, msg, item) :
	if doit :
		print(msg)
		print(item)
		print()

def vprint(msg) :
	print(msg) if Verbose else None


def execute(filename) :
	vprint("Executing ... \n")
	pgm = subprocess.Popen( ["sudo", "./build", filename] )
	pgm.wait()
	

prompt = "\n>>> "
history = []
histInd = -1
inhist = 0

def interactive() :
	global prompt, inhist
	print(Optimize)
	while True :
		text = input(prompt)
		history.append(text)
		if text.startswith("::") :
			handle(text[2:].split())
		else :
			try :
				if inhist :
					prompt, rest = prompt[:inhist], prompt[inhist:]
					inhist = 0
					text = rest + text
				run(text)
			except :
				print("Cannot interpret '" + text + "' !")
				translator.flush()

def handle(command) :
	head = command[0]
	if head == "s" :
		set(*command[1:])
	elif head == "q" :
		quit()
	elif head == "f" :
		flags(command[1:])
	elif head == "h" :
		global prompt, inhist
		inhist = len(prompt)
		prompt += history[int(command[1])]
	else :
		print("Hello")


def quit() :
	sys.exit()

def set(var, *val) :
	exec("global " + var + "\n" + var + " = " + " ".join(val))

def run(code) :
	writeTo("a.s", compile(code))
	execute("a")
	translator.flush()

def writeTo(filename, text) :
	with open(filename, "w") as file :
		file.write(text)

def oflags(arg) :
	global Optimize
	Optimize = optimizer.level = int(arg[2:]) if arg[2:] else 1
	optimizer.load(language + ".std")

def statflags(arg) :
	global lexemes, parseTree, unsugTree, optimTree, translation, flattened
	lexemes     = "L" in arg
	parseTree   = "P" in arg
	unsugTree   = "U" in arg or not arg[2:]
	optimTree   = "O" in arg
	translation = "T" in arg
	flattened   = "F" in arg

def flags(argv) :
	global Verbose, Generate
	for arg in argv :
		if arg.startswith("-O") :
			oflags(arg)
		elif arg.startswith("-d") :
			statflags(arg)
	Verbose   = "-V" in argv
	Generate  = not "-NG" in argv

if __name__ == "__main__" :
	argv = sys.argv

	# Compiled language
	language = argv[ argv.index("-l")+1 ] if "-l" in argv else "lang"

	# Loading the appropriate config files
	unsugarer.load(language + ".uns")
	lexer.load(language + ".lex")
	parser.load(language + ".par")

	# Various switches
	flags(argv)


	# Input
	if "-f" in argv :
		filename = argv[ argv.index("-f")+1 ]
		with open(filename, "r") as file :
			source = file.read()
	elif "--imm" in argv :
		source = argv[ argv.index("-imm")+1 ]
	elif "-I" in argv :
		interactive()
	else :
		source = input()

	# Output
	destination = "a.s" if not "-o" in argv else argv[ argv.index("-o")+1 ]


	result = compile(source)

	if "-E" in argv or "-o" in argv :
		writeTo(destination, result)

	if "-E" in argv :
		execute(destination[:-2])
