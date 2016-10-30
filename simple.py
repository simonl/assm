#!/usr/bin/python3

main = lambda :  ifthenelse(false)(lambda : 3)(lambda : 4)



zero = false = lambda a : lambda b : b
succ = lambda n : lambda f : lambda x : f(n(f)(x))
one = succ(zero)
two = succ(one)
three = succ(two)

plus = lambda m : lambda n : m(succ)(n)
times = lambda m : lambda n : m(plus(n))(zero)
expo = lambda m : lambda n : n(m)

true = lambda a : lambda b : a
ifthenelse = lambda p : lambda t : lambda e : p(t)(e)()

pair = lambda a : lambda b : lambda c : c(a)(b)
head = lambda p : p(true)
tail = lambda p : p(false)

def inc(n) :
	return n + 1

if __name__ == "__main__" :
	print( main() )
