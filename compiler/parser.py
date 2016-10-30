#!/usr/bin/python3



class Parser :
	def __init__(self, parser) :
		self.parser = parser

	def parse(self, tokens) :
		parseTree = self.parser(tokens)
		if parseTree :
			return parseTree[0]
		raise Exception("Could not parse! " + str(tokens))





def combAnd(parsers) :
	def parse(tokens) :
		parts = []
		for parser in parsers :
			result = parser(tokens)
			if not result :
				return None
			parts.append(result[0]) if result[0] != "***" else None
			tokens = result[1]
		return parts, tokens
	return parse

def combMany(parser) :
	def parse(tokens) :
		results = []
		while tokens :
			result = parser(tokens)
			if not result :
				break
			results.append(result[0]) if result[0] != "***" else None
			tokens = result[1]
		return results, tokens
	return parse

def combOpt(parser) :
	def parse(tokens) :
		result = parser(tokens)
		return ( [result[0]], result[1] ) if result else ([], tokens)
	return parse

def combOneOrMore(parser) :
	def parse(tokens) :
		results = []
		while tokens :
			result = parser(tokens)
			if not result :
				break
			results.append(result[0]) if result[0] != "***" else None
			tokens = result[1]
		if not results :
			return None
		return results, tokens
	return parse

def parseDrop(parser) :
	def parse(tokens) :
		result = parser(tokens)
		if result :
			return ("***", result[1])
	return parse

def combOr(parsers) :
	def parse(tokens) :
		for parser in parsers :
			result = parser(tokens)
			if result :
				return result
	return parse

def makeParser(tag, parser) :
	def parse(tokens) :
		result = parser(tokens)
		if result :
			return (tag, result[0]), result[1]
	return parse

def parseToken(const) :
	def parse(tokens) :
		if not tokens :
			return None
		return (tokens[0], tokens[1:]) if tokens[0][0] == const else None
	return parse

def parseString(string) :
	def parse(tokens) :
		if not tokens :
			return None
		return (tokens[0], tokens[1:]) if tokens[0][1] == string else None
	return parse



definitions = {}

def load(filename) :
	with open(filename) as file :
		text = file.readlines()
	return process(text)

def process(lines) :
	global definitions
	defs = [processline(line) for line in lines if valid(line)]
	for name, op, parser in defs :
		definitions[name] = parser if op == ":=" else makeParser(name, parser)
	
	par = Parser(definitions["program"])
	definitions = {}
	return par

def valid(line) :
	return line.strip() and not line.startswith("//")

def processline(line) :
	splitted = line.split()
	name = splitted[0]
	op = splitted[1]
	pattern = " ".join(splitted[2:])
	return (name, op, processpattern(pattern))




def processpattern(pattern) :
	pattern = pattern.strip()
	if "|" in pattern :
		return processOr( [pat.strip() for pat in pattern.split("|")] )
	elif " " in pattern :
		return processAnd( pattern.split() )
	elif pattern[0] == "!" :
		return processDrop( pattern[1:] )
	elif pattern[-1] == "*" :
		return processMany( pattern[:-1] )
	elif pattern[-1] == "+" :
		return processOneOM( pattern[:-1] )
	elif pattern[-1] == "?" :
		return processOpt( pattern[:-1] )
	elif pattern[0] == "<" and pattern[-1] == ">" :
		return processParser( definitions, pattern[1:-1] )
	elif pattern[0] == '"' and pattern[-1] == '"' :
		return processString( pattern[1:-1] )
	else :
		return processToken( pattern )

def processOr(altern) :
	return combOr( [processpattern(alt) for alt in altern] )

def processAnd(succes) :
	return combAnd( [processpattern(suc) for suc in succes] )

def processMany(single) :
	return combMany( processpattern(single) )

def processOneOM(single) :
	return combOneOrMore( processpattern(single) )

def processDrop(name) :
	return parseDrop( processpattern(name) )

def processOpt(name) :
	return combOpt( processpattern(name) )

def processParser(definitions, name) :
	def parse(tokens) :
		return definitions[name](tokens)
	return parse

def processToken(name) :
	return parseToken(name)

def processString(string) :
	return parseString(string)




def printf(tree, tab="") :
	type  = tree[0]
	parts = tree[1]
	print(tab, type)
	if type in definitions :
		for part in parts :
			printf(part, tab+"\t")
	else :
		print(tab+"\t", parts)
