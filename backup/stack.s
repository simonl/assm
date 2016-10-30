.section .data
.section .text

.globl _start

_start:
	movl %esp, %ebp
	cmp %ebp, %esp
	je true
	
	movl $0, %ebx
	jmp end

	true:
	movl $1, %ebx

	end:
	movl $1, %eax
	int $0x80
