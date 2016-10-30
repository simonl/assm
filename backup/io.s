.section .data

	prebin:	.ascii "b"
	.long 2
	prehex:	.ascii "0x"
	digits:	.ascii "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	power_10:
	.long 1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1

	nxt_line: .ascii "\n"

.section .text

.equ SYS_CALL, 0x80
.equ STD_IN, 0
.equ STD_OUT, 1
.equ STD_ERR, 2

.equ READ, 3
.equ WRITE, 4
.equ OPEN, 5
.equ CLOSE, 6

.globl __print__
.globl __input__
.globl __printc__
.globl __inputc__
.globl __ln__

.globl __bin__
.globl __oct__
.globl __hex__
.globl __dec__

.type __print__,@function
.type __input__,@function
.type __printc__,@function
.type __inputc__,@function
.type __ln__,@function

.type __bin__,@function
.type __oct__,@function
.type __hex__,@function
.type __dec__,@function


__print__: 	#print = (string){ write(STD_OUT, string) }
	pushl (%esp)
	movl $STD_OUT, 4(%esp)
__write__:	# write = (file, string) { Linux_write(WRITE, file, string, len(string)) }
	enter $0, $0
	movl $WRITE, %eax
	movl 8(%ebp), %ebx
	movl 12(%ebp), %ecx
	movl -4(%ecx), %edx
	int $SYS_CALL
	leave
	ret $8

__ln__:
	enter $0, $0
	pushl $nxt_line
	call __printc__
	leave
	ret


__input__:
	pushl (%esp)
	movl $STD_IN, 4(%esp)
__read__: 		#read = (file, buffer){ read(file, buffer, len(buffer)) }
	enter $0, $0
	movl 8(%ebp), %ebx
	movl 12(%ebp), %ecx
	movl -12(%ebp), %edx
	movl $READ, %eax
	int $SYS_CALL
	movl %ebp, %esp
	popl %ebp
	ret $8

__printc__: 		# printChar = (char){ putChar(STD_OUT, char) }
	pushl (%esp)
	movl $STD_OUT, 4(%esp)
__writec__: 		# putChar = (file, char){ Linux_write(file, char, 1) }
	enter $0, $0
	movl $WRITE, %eax
	movl 8(%ebp), %ebx
	movl 12(%ebp), %ecx
	movl $1, %edx
	int $SYS_CALL
	leave
	ret $8

__inputc__:
	pushl (%esp)
	movl $STD_IN, 4(%esp)
__readc__: 		# getChar = (file){ LINUX_READ(file, buffer, 1) }
	enter $0, $0
	movl $READ, %eax
	movl 8(%ebp), %ebx
	pushl $0
	movl %esp, %ecx
	movl $1, %edx
	int $SYS_CALL
	popl %eax
	leave
	ret $4

__bin__:	 #printNum = (num){ do{ num << 1 ; print(carry) }while(num) }
	pushl $prebin
	call __printc__
__binext__:
	enter $0, $0
	movl $32, %ecx
	print_loop:
		xorl %eax, %eax
		shll 8(%ebp)
		adcl $digits, %eax

		pushl %ecx
		pushl %eax
		call __printc__
		popl %ecx

		loop print_loop
	leave
	ret $4

__hex__:
	pushl $prehex
	call __print__
__hexext__:
	enter $0, $0
	movl $8, %ecx
	Hex_print_loop:
		roll $4, 8(%ebp)
		movl 8(%ebp), %eax

		andl $15, %eax		#extract last 4 bits from lower byte
		addl $digits, %eax

		pushl %ecx
		pushl %eax
		call __printc__
		popl %ecx

		loop Hex_print_loop
	end_hex_print:
	leave
	ret $4

__oct__:
	pushl $digits
	call __printc__
__octext__:
	enter $0, $0	#first 2 bits are special : 32bits = 10*3bits + 2bits
	roll $2, 8(%ebp)
	movl 8(%ebp), %eax
	andl $3, %eax

	movl $11, %ecx
	octal_loop:
		addl $digits, %eax
		pushl %ecx
		pushl %eax
		call __printc__
		popl %ecx

		roll $3, 8(%ebp)
		movl 8(%ebp), %eax
		andl $7, %eax

		loop octal_loop
	end_octal_loop:
	leave
	ret $4

__dec__:
	enter $4, $0
	movl $10, %ecx
	movl $0, -4(%ebp)
	dec_loop:
		movl $power_10, %ebx
		addl -4(%ebp), %ebx
		movl (%ebx), %ebx

		xorl %edx, %edx
		movl 8(%ebp), %eax
		divl %ebx, %eax
		movl %edx, 8(%ebp)

		addl $digits, %eax
		pushl %ecx
		pushl %eax
		call __printc__
		popl %ecx

		addl $4, -4(%ebp)
		loop dec_loop
	end_dec_loop:
	leave
	ret $4

# Not actually implemented

__open__:
	movl -4(%ebp), %ebx
	movl $03101, %ecx
	movl $0666, %edx
	movl $OPEN, %eax
	int $SYS_CALL

__close__:
	enter $0, $0
	movl $CLOSE, %eax
	movl 8(%ebp), %ebx
	int $SYS_CALL
	leave
	ret $4

