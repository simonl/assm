#!/usr/bin/python3

import re


def load(filename) :
	with open(filename, "r") as file :
		lines = [line.strip() for line in file]
		definitions = [ processline(line) for line in lines if line]
	return BestFitLexer(definitions)

def processline(line) :
	openquote = line.index('"')
	name = line[:openquote].strip()
	pattern = line[openquote+1:-1]
	return (name, re.compile(pattern))

class Lexer :
	def __init__(self, definitions, trash=["ws", "com"]) :
		self.definitions = definitions
		self.trash = trash

	def lex(self, input) :
		lexemes = []
		while input :
			name, length = self.nextToken(input)
			if name not in self.trash :
				lexemes.append( (name, input[:length]) )
			input = input[length:]
		return lexemes

	def lexIt(self, input) :
		while input :
			name, length = self.nextToken(input)
			if name not in self.trash :
				yield (name, input[:length])
			input = input[length:]

class FirstFitLexer(Lexer) :
	def nextToken(self, input) :
		for name, regex in self.definitions :
			match = regex.match(input)
			if match :
				return name, match.end()
		raise Exception("Cannot lex! " + str(input))

class BestFitLexer(Lexer) :
	def nextToken(self, input) :
		trials = []
		for name, regex in self.definitions :
			match = regex.match(input)
			if match :
				trials.append( (name, match.end()) )
		if trials :
			return max(trials, key=(lambda tok : tok[1]))
		raise Exception("Cannot lex! " + str(input))



left = lambda x, y : x >= y
right = lambda x, y : x > y

info = {"+" : ("+", 10, left),
	"^" : ("^", 20, right),
	"@" : ("@", 5, right),
	"[" : ("[", 50, right),
	"]" : ("]", 50, left)}

def prefix(symbol, precedence) :
	return infix(symbol, precedence, lambda x, y : x > y)

def postfix(symbol, precedence) :
	return infix(symbol, precedence, lambda x, y : x >= y)

def infix(symbol, precedence, assoc) :
	def do(operators, output) :
		while operators :
			op, prec = operators[-1]
			if assoc(prec, precedence) :
				output.append( op )
				operators.pop()
			else :
				break
		operators.append( (symbol, precedence) )
	return do

def outfix(entry, exit) :
	def do(operators, output) :
		while operators :
			op, prec = operators.pop()
			output.append( op )
			if op == entry :
				break
	return (lambda ops, out : out.append( (entry, 0) ), do)

def parse(tokens) :
	output = []
	operators = []
	for token in tokens :
		if token.isnumeric() :
			output.append(token)
		elif token == "(" :
			operators.append( (token, 100, lambda x, y : x > y) )
		elif token == ")" :
			symbol, prec, assoc = operators.pop()
			while symbol != "(" :
				output.append(symbol)
				symbol, prec, assoc = operators.pop()
			output.append(token)
		else :
			symbol, prec, assoc = info[token]
			if operators :
				sym, p, a = operators[-1]
				while assoc(p, prec) :
					output.append(sym)
					operators.pop()
					if operators :
						sym, p, a = operators[-1]
					else :
						break
			operators.append( (symbol, prec, assoc) )
	while operators :
		sym, *rest = operators.pop()
		output.append(sym)
	return output

# _ op	-> left
# op _	-> right
# _ op _ -> ? specify
# op _ op -> none

# @ 1 + 4

if __name__ == "__main__" :
	print(parse(input("> ").split()))
