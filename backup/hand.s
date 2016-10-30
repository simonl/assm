.section .data
.section .text
.globl _start

start:
	pushl _next
	pushl %ebp
	movl %esp, %ebp
	jmp main
	movl %eax, %ebx
	movl $1, %eax
	int $0x80

.type main,@function

main:
	movl $34, %eax
	movl %ebp, %esp
	popl %ebp
	ret

