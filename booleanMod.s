.section .data
.globl True
	True:
	.int 1
.globl False
	False:
	.int 0

.section .text

_ifTrue:
	movl $1, %eax
	ret

_ifFalse:
	xorl %eax, %eax
	ret

.globl _lesser
.globl _greater
.globl _equals
.globl _lesserEquals
.globl _greaterEquals
.globl _notEquals

_greater:
	cmp %eax, %ebx
	jg _ifTrue
	jmp _ifFalse

_lesser:
	cmp %eax, %ebx
	jl _ifTrue
	jmp _ifFalse

_equals:
	cmp %eax, %ebx
	je _ifTrue
	jmp _ifFalse

_lesserEquals:
	cmp %eax, %ebx
	jle _ifTrue
	jmp _ifFalse

_greaterEquals:
	cmp %eax, %ebx
	jge _ifTrue
	jmp _ifFalse

_notEquals:
	cmp %eax, %ebx
	jne _ifTrue
	jmp _ifFalse

.globl _or
.globl _and

_or:
	cmp False, %ebx
	jne _ifTrue
	cmp False, %eax
	jne _ifTrue
	jmp _ifFalse

_and:
	cmp False, %ebx
	je _ifFalse
	cmp False, %eax
	je _ifFalse
	jmp _ifTrue
