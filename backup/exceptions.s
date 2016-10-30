.section .data
	DEFAULT_HANDLER:
	.long EXC, (ADDR)
	EXC:
	.long Illegal_Argument_Exception
	ADDR:
	.long DEF_HANDLE

.globl Illegal_Argument_Exception
	Illegal_Argument_Exception:
	.ascii "Illegal_Argument_Exception\n\0"

.section .bss
	.lcomm my_buffer, 25

.section .text
.globl _start
.globl throw

.equ STDOUT, 1
.equ SYSCALL, 0x80
.equ SYS_WRITE, 4
.equ SYS_EXIT, 1

_start:
	#Write to screen
	movl $SYS_WRITE, %eax
	movl $STDOUT, %ebx
	movl $Illegal_Argument_Exception, %ecx
	movl $30, %edx
	int $SYSCALL

	#Exit
	movl %eax, %ebx
	movl $SYS_EXIT, %eax
	int $SYSCALL

throw:
	jmp _start

DEF_HANDLE:
	jmp _start


