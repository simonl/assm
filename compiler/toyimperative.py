


def main(text) :
	stmt, lbl, text = preprocess(text)
	print(evaluate(stmt, lbl, text))

from itertools import chain
def preprocess(lines) :
	statements = []
	labels     = {}
	output	   = []
	for line in lines :
		if ":" in line :
			colon = line.index(":")
			label = line[:colon].strip()
			labels[label] = len(statements)
			line = line[colon+1:].strip()
		if not line.strip() :
			continue

		if "include" in line :
			pos = line.index("include") + 7
			with open(line[7:].strip(), "r") as file :
				sts, lbs, txs = preprocess(file.readlines())
			statements += sts
			for k, v in lbs.items() :
				labels[k] = v
			output += txs
		elif "<-" in line :
			arrow = line.index("<-")
			destination = line[:arrow].strip()
			source      = expression(line[arrow+2:].strip())
			statements.append( ("assignment", destination, source) )
		elif "exit" in line :
			ret = line.index("exit")
			returned = line[ret+4:].strip()
			statements.append( ("exit", returned) )
		elif "goto" in line :
			goto = line.index("goto")
			destination = line[goto+4:].strip()
			statements.append( ("goto", destination) )
		elif "if" in line :
			scrutinee, dest = line.strip()[2:].split()
			statements.append( ("if", scrutinee, dest) )
		elif "unless" in line :
			scrutinee, dest = line.strip()[6:].split()
			statements.append( ("unless", scrutinee, dest) )
		elif "push" in line :
			var = line.strip()[4:].strip()
			statements.append( ("push", var) )
		elif "pop" in line :
			var = line.strip()[3:].strip()
			statements.append( ("pop", var) )
		elif "call" in line :
			func = line.strip()[4:].strip()
			statements.append( ("call", func) )
		elif "return" in line :
			returned = line.strip()[6:].strip()
			statements.append( ("return", returned) )
		output.append(line)
	return statements , labels, output

binops = "+-*/="
def expression(expr) :
	for op in binops :
		if op in expr :
			pos = expr.index(op)
			rand1 = expr[:pos].strip()
			rand2 = expr[pos+1:].strip()
			return (op, rand1, rand2)
	if expr.isnumeric() :
		return ("constant", int(expr))
	elif expr.strip() in ["false", "true"] :
		return ("constant", eval(expr))
	else :
		return ("variable", expr)


def evaluate(statements, labels, text, env={}, stack=[]) :
	pc = 0
	while True :
		inst = statements[pc]
		print("[" + str(pc) + "]\t" + text[pc].strip().ljust(20) + str(stack).ljust(10) + str(env))

		type = inst[0]
		if type == "exit" :
			return env[inst[1]]
		elif type == "assignment" :
			lhs, rhs = inst[1], inst[2]
			if rhs[0] == "constant" :
				env[lhs] = rhs[1]
			elif rhs[0] == "variable" :
				env[lhs] = env[rhs]
			elif rhs[0] == "+" :
				env[lhs] = env[rhs[1]] + env[rhs[2]]
			elif rhs[0] == "-" :
				env[lhs] = env[rhs[1]] - env[rhs[2]]
			elif rhs[0] == "=" :
				env[lhs] = env[rhs[1]] == env[rhs[2]]
			pc += 1
		elif type == "goto" :
			pc = labels[inst[1]]
		elif type == "if" :
			if env[inst[1]] :
				pc = labels[inst[2]]
			else :
				pc += 1
		elif type == "unless" :
			if env[inst[1]] :
				pc += 1
			else :
				pc = labels[inst[2]]
		elif type == "pop" :
			env[inst[1]] = stack.pop()
			pc += 1
		elif type == "push" :
			stack.append( env[inst[1]] )
			pc += 1
		elif type == "call" :
			stack.append( pc+1 )
			pc = labels[inst[1]]
		elif type == "return" :
			pc = stack.pop()
			stack.append( env[inst[1]] )
		else :
			raise Exception("OMG" + str(inst))


def getInput() :
	text = []
	line = 0
	while True :
		inp = input(str(line) + "\t")
		if inp :
			line += 1
			text.append(inp)
		else :
			break
	return text

import sys
if __name__ == "__main__" :
	argv = sys.argv
	if "-f" in argv :
		pos = argv.index("-f") + 1
		with open(argv[pos], "r") as file :
			sample = file.readlines()
	else :
		sample = getInput()
	main(sample)
