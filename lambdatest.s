.include "std.s"

.section .data
	plus:
	.long plus0
	.long Null
	minus:
	.long minus0
	.long Null
	times:
	.long times0
	.long Null
	div:
	.long div0
	.long Null
	mod:
	.long mod0
	.long Null
	square:
	.long sqr0
	.long Null
	True:
	.long true0
	.long Null
	False:
	.long false0
	.long Null
	cond:
	.long cond0
	.long Null
	cons:
	.long cons0
	.long Null
	Car:
	.long car0
	.long Null
	Cdr:
	.long cdr0
	.long Null
	one:
	.long 1
	far:
	.long one
	zero:
	.long zero0

.section .text

zero0:
	enter $0, $0
	xorl %eax, %eax
	leave
	ret $4

## LAMBDA CALCULUS
#
#	lambda :      \x.e
#	application : f x
#

## CLOSURE
#
#	f = ( code . env )
#

# let x = y in ...
# (\x. ... ) y

# if p then t else f
# ((if p) t) f

# true
# \t . \f . t

# false
# \t . \f . f

# if
# \p . \t . \f . ((p t) f) ()


__lambda__: # lambda(code, env)
	jmp __cons__ # return code:env


__thunk__:
	jmp __cons__

__apply__: #apply(function, argument)
	enter $0, $0
	movl 8(%ebp), %eax

	pushl 4(%eax) 	# env
	pushl 12(%ebp) 	# arg
	call __cons__	# newenv = arg:env
	pushl %eax

	movl 8(%ebp), %eax
	call *(%eax)		# code(newenv)

	leave
	ret $8

__force__:
	enter $0, $0
	movl 8(%ebp), %eax
	pushl 4(%eax)
	call *(%eax)
	leave
	ret $4

__get__: # get( list, n )
	enter $0, $0
	movl 8(%ebp), %eax
	movl 12(%ebp), %ecx
	get_loop:
		test %ecx, %ecx
		jz end_get
		movl 4(%eax), %eax
	jmp get_loop
	end_get:
	movl (%eax), %eax
	leave
	ret $8

		# (\x.(\y.x) 5) 4
#main: # main = (\().(\x.\y.x) 4 5)) ()
	enter $0, $0

	pushl Null
	pushl $lambda0
	call __thunk__

	pushl %eax
	call __force__

	leave
	ret $4


#lambda0:
	enter $0, $0
	movl 8(%ebp), %edx

	movl $4, %eax

	leave
	ret $4






minus0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $minus1
	call __lambda__
	leave
	ret $4

minus1:
	enter $0, $0
	movl 8(%ebp), %edx
	movl 4(%edx), %ecx
	movl (%ecx), %eax
	subl (%edx), %eax
	leave
	ret $4

plus0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $plus1
	call __lambda__
	leave
	ret $4
plus1:
	enter $0, $0
	movl 8(%ebp), %edx
	movl (%edx), %eax
	movl 4(%edx), %edx
	addl (%edx), %eax
	leave
	ret $4

times0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $times1
	call __lambda__
	leave
	ret $4

times1:
	enter $0, $0
	movl 8(%ebp), %edx
	movl (%edx), %eax
	movl 4(%edx), %edx
	mull (%edx)
	leave
	ret $4

div0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $div1
	call __lambda__
	leave
	ret $4

div1:
	enter $0, $0
	movl 8(%ebp), %ecx
	movl 4(%ecx), %edx
	movl (%edx), %eax
	xorl %edx, %edx
	divl (%ecx)
	leave
	ret $4

mod0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $mod1
	call __lambda__
	leave
	ret $4
mod1:
	enter $0, $0
	movl 8(%ebp), %ecx
	movl 4(%ecx), %edx
	movl (%edx), %eax
	xorl %edx, %edx
	divl (%ecx)
	movl %edx, %eax
	leave
	ret $4

sqr0:
	enter $0, $0
	movl 8(%ebp), %edx
	movl (%edx), %eax
	mull %eax
	leave
	ret $4


true0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $true1
	call __lambda__
	leave
	ret $4

true1:
	enter $0, $0
	movl 8(%ebp), %edx
	movl 4(%edx), %eax
	movl (%eax), %eax
	leave
	ret $4

false0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $false1
	call __lambda__
	leave
	ret $4

false1:
	enter $0, $0
	movl 8(%ebp), %edx
	movl (%edx), %eax
	leave
	ret $0

cond0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $cond1
	call __lambda__
	leave
	ret $4

cond1:
	enter $0, $0
	pushl 8(%ebp)
	pushl $cond2
	call __lambda__
	leave
	ret $4

cond2:
	enter $0, $0
	movl 8(%ebp), %edx
	pushl (%edx)
	movl 4(%edx), %edx
	pushl (%edx)
	movl 4(%edx), %edx
	pushl (%edx)
	call __apply__
	pushl %eax
	call __apply__

	pushl %eax
	call __force__

	leave
	ret $4

cons0:
	enter $0, $0
	pushl 8(%ebp)
	pushl $cons1
	call __lambda__
	leave
	ret $4
cons1:
	enter $0, $0
	pushl 8(%ebp)
	pushl $cons2
	call __lambda__
	leave
	ret $4
cons2:
	enter $0, $0
	movl 8(%ebp), %edx
	movl (%edx), %ecx
	movl 4(%edx), %edx
	pushl (%edx)
	movl 4(%edx), %edx
	pushl (%edx)
	pushl %ecx
	call __apply__
	pushl %eax
	call __apply__
	leave
	ret $4

car0:
	enter $0, $0
	movl 8(%ebp), %edx
	pushl $True
	pushl (%edx)
	call __apply__
	leave
	ret $4
cdr0:
	enter $0, $0
	movl 8(%ebp), %edx
	pushl $False
	pushl (%edx)
	call __apply__
	leave
	ret $4

putTrue:
	movl $True, %eax
	ret

putFalse:
	movl $False, %eax
	ret

__lgt__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx
	cmp %ebx, %eax
	jg lputTrue
	jmp lputFalse

lputTrue:
	movl $True, %eax
	ret $8

lputFalse:
	movl $False, %eax
	ret $8
