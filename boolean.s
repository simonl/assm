.section .data
	.globl False
	.globl True

	false: .long 0
	true: .long 1

.section .text

.globl __equ__
.globl __neq__
.globl __lt__
.globl __leq__
.globl __gt__
.globl __geq__

.globl __bool__
.globl __and__
.globl __or__
.globl __xor__
.globl __not__

.type __equ__,@function
.type __neq__,@function
.type __lt__,@function
.type __leq__,@function
.type __gt__,@function
.type __geq__,@function

.type __bool__,@function
.type __and__,@function
.type __or__,@function
.type __xor__,@function
.type __not__,@function

__caseTrue__:
	movl true, %eax
	ret $8

__caseFalse__:
	movl false, %eax
	ret $8

__equ__:
	movl 4(%esp), %eax
	cmp 8(%esp), %eax
	jne __caseFalse__
	jmp __caseTrue__

__neq__:
	movl 4(%esp), %eax
	cmp 8(%esp), %eax
	je __caseFalse__
	jmp __caseTrue__

__lt__:
	movl 4(%esp), %eax
	cmp 8(%esp), %eax
	jge __caseFalse__
	jmp __caseTrue__

__leq__:
	movl 4(%esp), %eax
	cmp 8(%esp), %eax
	jg __caseFalse__
	jmp __caseTrue__

__gt__:
	movl 4(%esp), %eax
	cmp 8(%esp), %eax
	jle __caseFalse__
	jmp __caseTrue__

__geq__:
	movl 4(%esp), %eax
	cmp 8(%esp), %eax
	jl __caseFalse__
	jmp __caseTrue__

# Logical operations

__bool__:
	movl 4(%esp), %eax
	pushl (%esp)
	cmp false, %eax
	je __caseFalse__
	jmp __caseTrue__

__and__:
	movl 4(%esp), %ebx
	movl 8(%esp), %eax
	cmp false, %eax
	je __caseFalse__
	cmp false, %ebx
	je __caseFalse__
	jmp __caseTrue__

__or__:
	movl 4(%esp), %ebx
	movl 8(%esp), %eax
	cmp false, %eax
	jne __caseTrue__
	cmp false, %ebx
	jne __caseTrue__
	jmp __caseFalse__

__xor__:
	movl 4(%esp), %ebx
	movl 8(%esp), %eax
	cmp false, %eax
	jne xor_continue
	cmp false, %ebx
	jne __caseFalse__
	jmp __caseTrue__
	xor_continue:
	cmp false, %ebx
	jne __caseTrue__
	jmp __caseFalse__

__not__:
	movl 4(%esp), %eax
	pushl (%esp)
	cmp false, %eax
	je __caseTrue__
	jmp __caseFalse__

