.data
	code:
	.int LAM, IND, 0

.text

.globl _start

_start:
	jmp _exit

	movl $code, %esi
	xorl %ebp, %ebp
	pushl $ABORT
	jmp main

_exit:
	xorl %ebx, %ebx
	xorl %eax, %eax
	incl %eax
	int $0x80

main:
	movl (%esi), %eax
	addl $4, %esi
	jmp *%eax

__alloc__:
	ret $4

# Instructions

APP:
	pushl $12
	call __alloc__		# Get a thunk cell (tag x code x env)
	movl $THUNK,  (%eax)
	movl (%esi), %ebx
	movl %ebx, 4(%eax)
	movl %ebp, 8(%eax)	# Copy current code and environment in thunk
	pushl %eax
	pushl $ARG		# Push the thunk as an argument
	movl 4(%esi), %eax
	addl $8, %esi
	jmp *%eax		# Keep going

APPi:
	movl (%esi), %ecx
	call getN		# Get Nth binding from environment
	pushl %eax
	pushl $ARG		# Push it on the stack
	movl 4(%esi), %eax
	addl $8, %esi
	jmp *%eax		# Keep going

LAM:
	popl %eax
	cmp $ARG, %eax
	je ARGopt
	pushl %eax	# Optimise immediate application

	pushl $12
	call __alloc__	# Get a closure cell (tag x code x env)
	movl $CLOS, (%eax)
	movl %esi, 4(%eax)
	movl %ebp, 8(%eax)
	popl %ebx
	jmp *%ebx	# Inspect the continuation stack

IND:
	movl (%esi), %ecx
	call getN		# Get Nth binding in current environment
	jmp *(%eax)		# Evaluate what it points to

getN:	# index in %ecx
	movl %ebx, %eax
	getLoop:
		test %ecx, %ecx
		jz endLoop
		movl 4(%eax), %eax	# Get the Nth cdr of the environment
		decl %ecx
		jmp getLoop
	endLoop:
	movl (%eax), %eax		# Extract the car
	ret

getESize:
	movl %ebp, %eax
	xorl %ecx, %ecx
	lenLoop:
		test %eax, %eax
		jz endLen
		movl 4(%eax), %eax
		incl %ecx
		jmp lenLoop
	endLen:
	ret


TUP:
	popl %eax
	cmp $FIELD, %eax
	je FIELDopt
	pushl %eax

	call getESize	# returns in %ecx
	incl %ecx
	shll $2, %ecx
	pushl %ecx
	pushl %ecx
	call __alloc__
	popl %ecx
	addl %eax, %ecx
	movl %ebp, %ebx
	mkTup:
		test %eax, %ecx
		je endTup
		subl $4, %ecx
		movl (%ebx), %edx
		movl %edx, (%ecx)
		movl 4(%ebx), %ebx
		jmp mkTup
	endTup:
	movl $TUPLE, (%eax)
	popl %ebx
	jmp *%ebx

PICK:
	pushl (%esi)
	pushl $FIELD
	movl 4(%esi), %eax
	addl $8, %esi
	jmp *%eax

# Continuations on the stack

ARG:	# Closure being applied in %eax
	movl 4(%eax), %esi
	movl 8(%eax), %ebp

ARGopt:	# Apply arg directly without allocating a closure
	pushl $8
	call __alloc__		# Get a cons cell (nil | pointer x cons cell)

	popl (%eax)
	movl %ebp, 4(%eax)	# extend environment
	movl %eax, %ebp

	movl (%esi), %eax	# Fetch the instruction
	addl $4, %esi
	jmp *%eax		# Evaluate the closure

FIELD:
	popl %ebx
	addl %ebx, %eax
	jmp *(%eax)

FIELDopt:
	call getESize
	popl %ebx
	subl %ebx, %ecx
	call getN
	jmp *(%eax)

UPD:	# closure in %eax
	popl %ebx		# Pop pointer to update
	movl $INDIRECT, (%ebx)
	movl %eax, 4(%ebx)

TUPLE:	# Tuple is in %eax
CLOS:	# Closure is in %eax
	popl %ebx
	jmp *%ebx		# Keep on looking down the stack

# Values on the heap
ABORT:
VOID:
	jmp _exit

THUNK:  # Thunk is in %eax	= (THUNK * code * env)
	movl $VOID, (%eax)	# Void the tag while evaluating
	movl 4(%eax), %esi
	movl 8(%eax), %ebp	# Set up code and environment

	pushl %eax
	pushl $UPD		# Push an update notice for the thunk

	movl (%esi), %eax	# Fetch next instruction
	addl $4, %esi
	jmp *%eax		# Evaluate the thunk

INDIRECT:	# Indirection in %eax = (INDIRECT, *obj)
	movl 4(%eax), %eax
	jmp *(%eax)
