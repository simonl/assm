.section .data

	prebin:	.ascii "b"
	.long 2
	prehex:	.ascii "0x"
	digits:	.ascii "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	power_10:
	.long 1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1

	nxt_line: .ascii "\n"

	.long 2
	bang: .ascii "!\n"

.section .bss
	.lcomm __xbuffer__, 500

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
.globl __println__

.globl __bin__
.globl __oct__
.globl __hex__
.globl __dec__

.type __print__,@function
.type __input__,@function
.type __printc__,@function
.type __inputc__,@function
.type __ln__,@function
.type __println__,@function

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
	call __print__
	leave
	ret

__alert__:
	enter $0, $0
	pushl $bang
	call __print__
	leave
	ret

__println__:
	enter $0, $0
	pushl 8(%ebp)
	call __print__
	call __ln__
	leave
	ret $4

__input__:
	pushl (%esp)
	movl $STD_IN, 4(%esp)
__read__: 		#read = (file, buffer){ read(file, buffer, len(buffer)) }
	enter $0, $0

	movl $READ, %eax
	movl 8(%ebp), %ebx
	movl $__xbuffer__, %ecx
	movl $500, %edx
	int $SYS_CALL
	decl %eax

	pushl %eax
	call __buffToStr__

	leave
	ret $4

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



# Using the ExtremeBuffer

__buffToStr__:	# Specify the length to take
	enter $0, $0
	pushl 8(%ebp)
	call __alloc__
	pushl %eax
	pushl $__xbuffer__
	call __cp__
	leave
	ret $4

__buffToNum__: #jumped to
	enter $0, $0
	pushl 8(%ebp)
	call __buffToStr__
	pushl %eax
	call __rev__
	leave
	ret $4

# Numbers to String

__bin__:
	enter $0, $0
	movl 8(%ebp), %eax
	movl $__xbuffer__, %ebx
	movl $1, %ecx
	bin_loop:
		movl $digits, %edx

		shrl %eax
		jnc putZero
		incl %edx
		putZero:

		movb (%edx), %dl
		movb %dl, (%ebx)

		incl %ebx
		incl %ecx
		test %eax, %eax
		jnz bin_loop
	movb $'b', (%ebx)
	pushl %ecx
	call __buffToNum__
	leave
	ret $4

__oct__:
	enter $0, $0
	movl 8(%ebp), %eax
	movl $__xbuffer__, %ebx
	movl $1, %ecx
	oct_loop:
		movl %eax, %edx
		andl $7, %edx
		addl $digits, %edx

		movb (%edx), %dl
		movb %dl, (%ebx)

		incl %ebx
		incl %ecx
		shrl $3, %eax
		jnz oct_loop
	movb $'0', (%ebx)
	pushl %ecx
	call __buffToNum__
	leave
	ret $4


__hex__:
	enter $0, $0
	movl 8(%ebp), %eax
	movl $__xbuffer__, %ebx
	movl $2, %ecx
	hex_loop:
		movl %eax, %edx
		andl $0xf, %edx
		addl $digits, %edx

		movb (%edx), %dl
		movb %dl, (%ebx)

		incl %ebx
		incl %ecx
		shrl $4, %eax
		jnz hex_loop
	movb $'x', (%ebx)
	movb $'0', 1(%ebx)
	pushl %ecx
	call __buffToNum__
	leave
	ret $4

__dec__:
	enter $0, $0

	movl 8(%ebp), %eax
	movl $__xbuffer__, %ebx
	xorl %ecx, %ecx
	movl $10, %esi
	deci_loop:
		xorl %edx, %edx
		divl %esi
		addl $digits, %edx

		movb (%edx), %dl
		movb %dl, (%ebx)

		incl %ebx
		incl %ecx

		test %eax, %eax
		jnz deci_loop
	pushl %ecx
	call __buffToNum__
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

# Shouldn't be here

__ispowof2__: # number in %eax
	movl 4(%esp), %eax

	test %eax, %eax
	jz caseZ	#if zero, false

	movl %eax, %ebx
	decl %ebx
	andl %ebx, %eax
	jz ispow	#if zero, true
	xorl %eax, %eax
	caseZ:
	ret
	ispow:
	incl %eax
	ret
