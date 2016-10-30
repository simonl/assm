.include "std.s"

.section .data

	.long 12
	ftype:
	.ascii "<closure at "

	.long 1
	consop:
	.ascii ":"

	.long 1
	fend:
	.ascii ">"

	.long 0
	empty:
	.long 0

	function:
	.long empty
	.long lambda0

	.long 8
	globalContext:
	.long Null
	.long Null

	counter:
	.long globalContext
	.long thunk1

	factorial:
	.long globalContext
	.long lambda0

	adder:
	.long globalContext
	.long lambda1

	main007:
	.long globalContext
	.long main

	seven:
	.long globalContext
	.long thunk0

.section .text

#subs :
#	f -> return locals[f]
#		movl 'f'(%ebp), %eax
#		ret
#
#	(\z e) -> return ( locals++[z] : *subs(e) )
#		pushl $lambda_e
#		pushl 8(%ebp)
#		call __extend__
#		pushl %eax
#		call __cons__
#
#	(f x) -> return apply(subs(f), subs(x))
#		push subs(x)
#		push subs(f)
#		jmp __apply__

__call__: # call(closure, args...){ closure[1]( closure[0] ++ args ) }
	enter $0, $0
	movl 8(%ebp), %eax
	pushl 4(%eax)

	pushl 12(%ebp)
	pushl (%eax)
	call __concat__

	popl %ebx
	pushl %eax
	call *%ebx

	leave
	ret $8

__vcall__: # vcall(closure){ closure[1]( closure[0] ) }
	enter $0, $0
	movl 8(%ebp), %eax

	pushl (%eax)
	call *4(%eax)

	leave
	ret $4

__inherit__:
	enter $0, $0
	pushl $Null
	pushl 8(%ebp)
	call __cons__
	leave
	ret $4

# this@[parent, locals...] -> [this, params...]

# (\x  -> ...) == lambda
#	lambda(function, env)
# (\() -> ...) == thunk
#	thunk(function, env)
__enclose__:
	enter $0, $0

	pushl 8(%ebp)
	pushl 12(%ebp)
	call __inherit__
	pushl %eax
	call __cons__

	leave
	ret $8

# (\() ((\x (\y y)) 2) 4))
main:
	enter $8, $0

	pushl $counter
	call __vcall__
	movl %eax, -4(%ebp)

	pushl $counter
	call __vcall__
	movl %eax, -8(%ebp)

	movl $5, %ecx
	test_counters:
	pushl %ecx

		pushl -4(%ebp)
		call __vcall__
		pushl %eax
		call __pdec__
		call __ln__

		pushl -8(%ebp)
		call __vcall__
		pushl %eax
		call __pdec__
		call __ln__

	popl %ecx
	loop test_counters

	pushl %ebp
	pushl $Illegal_Argument_Exception
	call __except__
	pushl %eax
	jmp throw

	xorl %eax, %eax
	leave
	ret $4


thunk0:
	enter $0, $0

	movl $7, %eax

	leave
	ret $4

thunk1:		# counter(){ var count = 0; return (){ return ++count } }
	enter $0, $0

	pushl $0
	pushl 8(%ebp)
	call __append__

	pushl %eax
	pushl $thunk2
	call __enclose__

	leave
	ret $4

thunk2:
	enter $0, $0
	movl 8(%ebp), %ebx
	movl (%ebx), %ebx
	movl 8(%ebx), %eax
	incl 8(%ebx)
	leave
	ret $4

# ((\x (\y y)) 2) 4)
lambda0:
	enter $0, $0
	movl 8(%ebp), %ebx

	movl (%ebx), %ecx
	movl $1, %eax
	fact_loop:
		test %ecx, %ecx
		jz end_fact_loop

		mull %ecx

		decl %ecx
		jmp fact_loop
	end_fact_loop:
	leave
	ret $4

# (\y x+y) <- x
lambda1:
	enter $0, $0

	pushl 8(%ebp)
	pushl $lambda2
	call __enclose__
	pushl %eax

	leave
	ret $4

# (\y y)
lambda2:
	enter $0, $0
	movl 8(%ebp), %ebx

	movl (%ebx), %eax
	addl 4(%ebx), %eax

	leave
	ret $4




__plambda__:
	enter $0, $0

	pushl $fend
	pushl 8(%ebp)
	pushl $ftype
	call __print__
	call __ppair__
	call __print__

	leave
	ret $4

__ppair__:
	enter $0, $0
	movl 8(%ebp), %eax

	pushl 4(%eax)
	pushl $consop
	pushl (%eax)
	call __phex__
	call __print__
	call __phex__

	leave
	ret $4

# calling a closure ->
#	push arg1
#	push arg2
#	...
#	push (car closure)
#	call (cdr closure)
