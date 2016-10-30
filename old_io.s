.section .data
.section .text

.equ SYS_CALL, 0x80
.equ STD_IN, 0
.equ STD_OUT, 1
.equ STD_ERR, 2

.equ READ, 3
.equ WRITE, 4
.equ OPEN, 5
.equ CLOSE, 6

.globl __pbin__
.globl __poct__
.globl __phex__
.globl __pdec__

.type __pbin__,@function
.type __poct__,@function
.type __phex__,@function
.type __pdec__,@function



__pbin__:	 #printNum = (num){ do{ num << 1 ; print(carry) }while(num) }
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

__phex__:
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

__poct__:
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

__pdec__:
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
