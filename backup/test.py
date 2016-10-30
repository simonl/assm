
def func() :
	return (0, (1, 2))


if __name__ == "__main__" :
	a, (b, c) = func()
	print(a, b, c)
