.section .data
	.globl Zero
	.globl One

	Zero: .long 0
	One: .long 1

.section .text

.globl __add__
.globl __sub__
.globl __mul__
.globl __div__
.globl __mod__
.globl __pow__
.globl __sqr__
.globl __sqrt__
.globl __inc__
.globl __decr__
.globl __neg__
.globl __inv__
.globl __abs__

.globl __shl__
.globl __shr__
.globl __rol__
.globl __ror__

.globl __band__
.globl __bor__
.globl __bxor__
.globl __bnot__

.type __add__,@function
.type __sub__,@function
.type __mul__,@function
.type __div__,@function
.type __mod__,@function
.type __pow__,@function
.type __sqr__,@function
.type __sqrt__,@function
.type __inc__,@function
.type __decr__,@function
.type __neg__,@function
.type __inv__,@function
.type __abs__,@function

.type __band__,@function
.type __bor__,@function
.type __bxor__,@function
.type __bnot__,@function

__add__:
	movl 4(%esp), %eax
	addl 8(%esp), %eax
	ret $8

__sub__:
	movl 4(%esp), %eax
	subl 8(%esp), %eax
	ret $8

__mul__:
	movl 4(%esp), %eax
	mull 8(%esp)
	ret $8

__div__:
	xorl %edx, %edx
	movl 4(%esp), %eax
	divl 8(%esp)
	ret $8

__mod__:
	xorl %edx, %edx
	movl 4(%esp), %eax
	divl 8(%esp)
	movl %edx, %eax
	ret $8

__pow__:
	movl 8(%esp), %ebx
	test %ebx, %ebx
	jnz doPower

	movl $1, %eax
	ret $8

	doPower:
	movl 4(%esp), %eax
	movl $1, %ecx

	pow_loop:
		cmp $1, %ebx
		je end

		shr %ebx
		jnc squaring

		movl %eax, %esi

		mull %ecx
		movl %eax, %ecx

		movl %esi, %eax
		squaring:
		mull %eax

		jmp pow_loop
	end:
	mull %ecx
	ret $8

__sqr__:
	movl 4(%esp), %eax
	mull %eax
	ret $4

__sqrt__:
	movl 4(%esp), %eax
	ret $4

__succ__:
	movl 4(%esp), %eax
	incl %eax
	ret $4

__pred__:
	movl 4(%esp), %eax
	decl %eax
	ret $4

__neg__:
	movl 4(%esp), %eax
	negl %eax
	ret $4

__inv__:
	movl 4(%esp), %eax
	notl %eax
	ret $4

__abs__:
	cmp $0, 4(%esp)
	jl __neg__
	movl 4(%esp), %eax
	ret $4


# Bitwise operations
__band__:
	movl 4(%esp), %eax
	andl 8(%esp), %eax
	ret $8

__bor__:
	movl 4(%esp), %eax
	orl 8(%esp), %eax
	ret $8

__bxor__:
	movl 4(%esp), %eax
	xorl 8(%esp), %eax
	ret $8

__bnot__:
	movl 4(%esp), %eax
	notl %eax
	ret $4

__shl__:
	movl 4(%esp), %eax
	movl 8(%esp), %ecx
	shl:
		shll %eax
	loop shl
	ret $8

__shr__:
	movl 4(%esp), %eax
	movl 8(%esp), %ecx
	shr:
		shrl %eax
	loop shr
	ret $8

__ror__:
	movl 4(%esp), %eax
	movl 8(%esp), %ecx
	ror:
		rorl %eax
	loop ror
	ret $8

__rol__:
	movl 4(%esp), %eax
	movl 8(%esp), %ecx
	rol:
		roll %eax
	loop rol
	ret $8
