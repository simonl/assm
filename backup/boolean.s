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
	leave
	ret

__caseFalse__:
	movl false, %eax
	leave
	ret

__equ__:
	popl %ebx
	popl %eax
	cmp %ebx, %eax
	jne __caseFalse__
	jmp __caseTrue__

__neq__:
	popl %ebx
	popl %eax
	cmp %ebx, %eax
	je __caseFalse__
	jmp __caseTrue__

__lt__:
	enter $0, $0
	movl 8(%ebp), %ebx
	movl 12(%ebp), %eax
	cmp %ebx, %eax
	jge __caseFalse__
	jmp __caseTrue__

__leq__:
	popl %ebx
	popl %eax
	cmp %ebx, %eax
	jg __caseFalse__
	jmp __caseTrue__

__gt__:
	popl %ebx
	popl %eax
	cmp %ebx, %eax
	jle __caseFalse__
	jmp __caseTrue__

__geq__:
	popl %ebx
	popl %eax
	cmp %ebx, %eax
	jl __caseFalse__
	jmp __caseTrue__

# Logical operations

__bool__:
	popl %eax
	cmp false, %eax
	je __caseFalse__
	jmp __caseTrue__

__and__:
	popl %ebx
	popl %eax
	cmp false, %eax
	je __caseFalse__
	cmp false, %ebx
	je __caseFalse__
	jmp __caseTrue__

__or__:
	popl %ebx
	popl %eax
	cmp false, %eax
	jne __caseTrue__
	cmp false, %ebx
	jne __caseTrue__
	jmp __caseFalse__

__xor__:
	popl %ebx
	popl %eax
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
	popl %eax
	cmp false, %eax
	je __caseTrue__
	jmp __caseFalse__

