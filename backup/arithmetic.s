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
	enter $0, $0
	movl 8(%ebp), %eax
	movl 12(%ebp), %ebx
	addl %ebx, %eax
	leave
	ret

__sub__:
	popl %ebx
	popl %eax
	subl %ebx, %eax
	leave
	ret

__mul__:
	enter $0, $0
	movl 8(%ebp), %eax
	movl 12(%ebp), %ebx
	imull %ebx, %eax
	leave
	ret

__div__:
	popl %ebx
	popl %eax
	idivl %ebx, %eax
	leave
	ret

__mod__:
	popl %ebx
	popl %eax
	idivl %ebx, %eax
	movl %edx, %eax
	leave
	ret

__pow__:
	popl %ebx
	cmp $0, %ebx
	jne doPower

	movl $1, %eax
	leave
	ret

	doPower:
	popl %eax
	movl $1, %ecx

	pow_loop:
		cmp $1, %ebx
		je end

		shr %ebx
		jnc squaring
		
		imull %eax, %ecx
		squaring:
		imull %eax, %eax
		
		jmp pow_loop
	end:
	imull %ecx, %eax
	leave
	ret

__sqr__:
	popl %eax
	imull %eax, %eax
	leave
	ret

__sqrt__:
	popl %eax
	leave
	ret

__inc__:
	enter $0, $0
	movl 8(%ebp), %eax
	incl (%eax)
	movl (%eax), %eax
	leave
	ret

__decr__:
	popl %eax
	decl %eax
	leave
	ret

__neg__:
	popl %eax
	negl %eax
	leave
	ret

__inv__:
	popl %eax
	notl %eax
	leave
	ret

__abs__:
	cmp $0, -4(%ebp)
	jl __neg__
	popl %eax
	leave
	ret


# Bitwise operations
__band__:
	popl %eax
	popl %ebx
	andl %ebx, %eax
	leave
	ret

__bor__:
	popl %eax
	popl %ebx
	orl %ebx, %eax
	leave
	ret

__bxor__:
	popl %eax
	popl %ebx
	xorl %ebx, %eax
	leave
	ret

__bnot__:
	popl %eax
	notl %eax
	leave
	ret

