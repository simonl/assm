.section .data
.section .text

.globl __rasg
.globl __as__

.globl __inc__
.globl __decr__
.globl __addasg__
.globl __subasg__
.globl __mulasg__
.globl __divasg__
.globl __modasg__
.globl __powasg__

.globl __bxorasg__
.globl __bandasg__
.globl __borasg__
.globl __bnotasg__

.type __rasg__,@function
.type __as__,@function

.type __inc__,@function
.type __decr__,@function
.type __addasg__,@function
.type __subasg__,@function
.type __mulasg__,@function
.type __divasg__,@function
.type __modasg__,@function
.type __powasg__,@function

__rasg__:
	movl 4(%esp), %ebx
	movl 8(%esp), %eax
	movl %eax, (%ebx)
	ret $8

__as__:
	movl 4(%ebp), %eax
	movl 8(%ebp), %ebx
	movl %eax, (%ebx)
	ret $8

__inc__:
	movl 4(%esp), %eax
	incl (%eax)
	movl (%eax), %eax
	ret $4

__decr__:
	movl 4(%esp), %eax
	decl (%eax)
	movl (%eax), %eax
	ret $4

__addasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx
	addl %ebx, (%eax)
	movl (%eax), %eax
	ret $8

__subasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx
	subl %ebx, (%eax)
	movl (%eax), %eax
	ret $8

__negasg__:
	movl 4(%esp), %eax
	notl (%eax)
	movl (%eax), %eax
	ret $4

__mulasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx
	movl (%eax), %eax
	mull %ebx
	movl %eax, (%eax)
	ret $8

__divasg__:
	movl 4(%esp), %ecx
	movl 8(%esp), %ebx
	xorl %edx, %edx
	movl (%ecx), %eax
	divl %ebx
	movl %eax, (%ecx)
	ret $8

__modasg__:
	movl 4(%esp), %ecx
	movl 8(%esp), %ebx
	xorl %edx, %edx
	movl (%ecx), %eax
	divl %ebx
	movl %edx, (%ecx)
	ret $8

__invasg__:
	movl 4(%esp), %eax
	notl (%eax)
	movl (%eax), %eax
	ret $4

__powasg__:
	pushl 8(%esp)
	movl 4(%esp), %eax
	pushl (%eax)
	call __pow__
	movl 4(%esp), %ebx
	movl %eax, (%ebx)
	ret $8


#bitwise ops

__bandasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx
	andl %ebx, (%eax)
	movl (%eax), %eax
	ret $8

__bxorasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx
	xorl %ebx, (%eax)
	movl (%eax), %eax
	ret $8

__borasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx
	orl %ebx, (%eax)
	movl (%eax), %eax
	ret $8

__bnotasg__:
	movl 4(%esp), %eax
	notl (%eax)
	movl (%eax), %eax
	ret $4

__shrasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ecx
	shiftr:
		shrl (%eax)
	loop shiftr
	movl (%eax), %eax
	ret $8

__shlasg__:
	movl 4(%esp), %eax
	movl 8(%esp), %ecx
	shiftl:
		shll (%eax)
	loop shiftl
	movl (%eax), %eax
	ret $8

__rollasg__:
	movl 4(%esp), %ebx
	movl 8(%esp), %ecx
	movl (%ebx), %eax
	roll:
		roll %eax
	loop roll
	movl %eax, (%ebx)
	ret $8

__rolrasg__:
	movl 4(%esp), %ebx
	movl 8(%esp), %ecx
	movl (%ebx), %eax
	rolr:
		rorl %eax
	loop rolr
	movl %eax, (%ebx)
	ret $8
