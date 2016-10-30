.section .data
	DEFAULT_HANDLER:
	.long Null, DEF_HANDLE
	EXC:
	.long Illegal_Argument_Exception
	ADDR:
	.long DEF_HANDLE

	Illegal_Argument_Exception:
	.long IAE
	.long Null

	.long 27
	IAE:
	.ascii "Illegal Argument Exception!"


.section .bss
	.lcomm my_buffer, 25

.section .text
.globl _start
.globl throw

.equ STDOUT, 1
.equ SYSCALL, 0x80
.equ SYS_WRITE, 4
.equ SYS_EXIT, 1

_start122:
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

throw: #throw(Exception)
	movl (%esp), %eax
	movl %eax, DEFAULT_HANDLER

	movl $HANDLER_STACK, %ebx
	next_handler:
	movl (%ebx), %ecx #car(stack)
		cmp %eax, (%ecx)
		je handle
		movl 4(%ebx), %eax #stack = cdr(stack)
	jmp next_handler
	handle: #handler in %ecx

	jmp *4(%ecx)


__except__: # constructs Exception e->[Type,Frame]
	enter $0, $0
	movl 8(%ebp), %eax
	movl 12(%ebp), %ebx
	movl %ebx, 4(%eax)
	leave
	ret $8

DEF_HANDLE: #handle(Exception e){ print(e); crash; }
	pushl (%eax)
	call __println__

	movl $1, %eax
	jmp __exit__

