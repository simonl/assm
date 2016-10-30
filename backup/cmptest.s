.section .data

.section .text

.globl _start

_start:
	movl $1, %eax
	cmpl $0, %eax
	jl false

	true:
	movl $1, %ebx
	jmp end

	false:
	movl $0, %ebx
	
	end:
	movl $1, %eax
	int $0x80

