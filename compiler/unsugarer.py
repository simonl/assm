import lexer
import parser

unsLexer = None
unsParser = None


class Unsugarer :
	def __init__(self, definitions) :
		self.definitions = definitions

	def unsugar(self, tree, dict={}) :
		(type, parts) = tree
		if type in self.definitions.keys() :
			dict["_parts"] = parts
			dict["_unsugar"] = self.unsugar
			params, processor = self.definitions[type]
			for param, part in zip(params, parts) :
				dict[param] = part
			return processor(dict)
		return tree


definitions = {}
from functools import reduce

def foldr(f, d, xs) :
	for x in reversed(xs) :
		d = f(x, d)
	return d


builtins = {
	"add" : lambda *xs : reduce(operator.__add__, xs),
	"len" : lambda ls : len(ls),
	"type" : lambda node : node[0],
	"cons" : lambda x, xs : (x, xs),
	"car" : lambda xs : xs[0],
	"cdr" : lambda xs : xs[1:],
	"eq" : lambda x, y : x == y,
	"gt" : lambda x, y : x > y,
	"lt" : lambda x, y : x < y,
	"le" : lambda x, y : x <= y,
	"ge" : lambda x, y : x >= y,
	"ne" : lambda x, y : x != y,
	"max" : lambda x,y : max(x,y),
	"min" : lambda x,y : min(x,y),
	"error" : lambda msg : print(msg),
	"branch" : lambda n, t : t[1][n],
	"branches" : lambda t : t[1],
	"type" : lambda t : t[0],
	"insert" : lambda e, es : [e] + es,
	"index" : lambda e, es : es.index(e),
	"append" : lambda e, es : es + [e],
	"lookup" : lambda f : builtins[f],
	"map" : lambda f, xs : [f(x) for x in xs],
	"filter" : lambda p, xs : [x for x in xs if p(x)],
	"foldl" : lambda f, b, xs : reduce(f, xs, b),
	"foldr" : lambda f, b, xs : foldr(f, b, xs),
	"set" : lambda binding, val : exec("builtins[binding] = val")
	}

def load(filename) :
	global definitions, unsLexer, unsParser
	
	if not (unsLexer and unsParser) :
		unsLexer = lexer.load("unsugarer.lex")
		unsParser = parser.load("unsugarer.par")

	with open(filename, "r") as file :
		text = file.read()

	trees = unsParser.parse(unsLexer.lex(text))
	parsers = [process(tree) for tree in trees]

	for name, params, processor in [x for x in parsers if x] :
		definitions[name] = list(map(lambda x : x[1], params)), processor


	uns = Unsugarer(definitions)
	definitions = {}
	return uns

def process(tree) :
	type = tree[0]
	parts = tree[1]

	if type == "definition" :
		makeDefinition(parts[0][1], process(parts[1]))
	elif type == "defun" :
		makeDefinition(parts[0][1], makeFunction(parts[1], process(parts[2])))
	elif type == "rule" :
		return (parts[0][1], parts[1], makeUnsug(process(parts[2])))
	elif type == "action" :
		return (parts[0][1], parts[1], process(parts[2]))
	elif type == "continue" :
		return (parts[0][1], goDeeper(parts[0][1]))
	elif type == "function" :
		return makeFunction(parts[0], process(parts[1]))
	elif type == "name" :
		return makeLookup(parts)
	elif type == "argument" :
 		return select( makeLookup("_parts"), takeelem(int(parts[1:])) )
	elif type == "unsugar" :
		return makeUnsug(process(parts[0]))
	elif type == "assignment" :
		return makeAssign(parts[0][1], process(parts[1]))
	elif type == "sequence" :
		return makeSeq([process(part) for part in parts[0]])
	elif type == "all" :
		return makeLookup("_parts")
	elif type == "list" :
		return makeList( [process(part) for part in parts[0]] )
	elif type == "call" :
		return makecall(process(parts[0]), [process(part) for part in parts[1]])
	elif type == "range" :
		return takerange(int(parts[0][1]), int(parts[1][1]))
	elif type == "string" :
		return id(parts[1:-1])
	elif type == "item" :
		return takeelem(int(parts[1]))
	elif type == "select" :
		return select(process(parts[0]), process(parts[1]))
	elif type == "leaf" :
		return makeTuple( parts[0][1], [process(field) for field in parts[1]] )
	elif type == "conditional" :
		return makeCond(*[process(part) for part in parts])
	elif type == "node" :
		return makeNode(parts[0][1], makeList( [process(part) for part in parts[1]] ))
	elif type == "number" :
		return id(int(parts))

def makeDefinition(name, body) :
	global builtins
	builtins[name] = body({})

def makeSeq(steps) :
	def unsug(dict) :
		res = [step(dict) for step in steps]
		return res[-1]
	return unsug

def makeAssign(var, val) :
	def unsug(dict) :
		dict[var] = val(dict)
		return dict[var]
	return unsug

def makeFunction(formals, body) :
	formals = [str for typ, str in formals]
	def thunk(dict) :
		dict = dict.copy()
		def call(*args) :
			for formal, arg in zip(formals, args) :
				dict[formal] = arg
			return body(dict)
		return call
	return thunk
		

def makeCond(pred, then, els) :
	return (lambda dict : then(dict) if pred(dict) else els(dict) )

def id(x) :
	return (lambda dict : x)

def makeUnsug(pattern) :
	return (lambda dict  : dict["_unsugar"](pattern(dict), dict.copy()) )

def makeLookup(name) :
	return (lambda dict : dict[name] if name in dict else builtins[name])

def makecall(func, args) :
	return (lambda dict : func(dict)( *[arg(dict) for arg in args] ) )

def select(fro, elem) :
	return (lambda dict : elem(fro(dict)) )

def takeelem(elem) :
	return (lambda parts : parts[elem])

def takerange(fro, to1) :
	def unsug(parts) :
		to = to1 if to1 != 0 else len(parts)
		return [part for part in parts[fro:to]]
	return unsug

def goDeeper(type) :
	return (lambda dict : (type, [dict["_unsugar"](part) for part in dict["_parts"]]) )

def makeNode(type, cons) :
	return (lambda dict : (type, cons(dict)) )

def makeList(elems) :
	return (lambda dict : [elem( dict ) for elem in elems])

def makeTuple(head, elems) :
	return (lambda dict : tuple( [head] + [elem(dict) for elem in elems] ))




test = ("letexpression", [
		("variable", "x"), 
		("lambda", [("variable", "y"), ("variable", "y")]),
		[	[("variable", "z"), 
			 ("lambda", [("variable", "y"), ("variable", "y")])]
		],
		("variable", "x")])

if __name__ == "__main__" :
	unser = load("lang.uns")
	print(
		unser.unsugar( test )
	)	
