.section .data
.section .text

.globl _start

_start:
	movl %esp, %ebp
	pushl $4
	pushl $1
	pushl $2
	movl %ebp, %eax
	subl $4, %eax
	movl (%eax), %ebx
	movl $1, %eax
	int $0x80
