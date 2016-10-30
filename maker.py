#!/usr/bin/python3

def makeVar(var) :
	return ("variable", var)

def makeThunk(tree) :
	return ("thunk", ["", "", "", "", tree, ""])

def makeLambda(var, tree) :
	return ("lambda", ["", "", makeVar(var), "", tree, ""])

def makeApply(e1, e2) :
	return ("apply", ["", e1, e2, ""])

def makeForce(thunk) :
	return ("force", ["", thunk, ""])
