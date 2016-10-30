.include "std.s"
.section .data
.section .text
.globl _start
_start:
pushl $0
movl %esp, %ebp
call main
movl %eax, %ebx
movl $1, %eax
int $0x80
	#FUNCTION main
.type main,@function
	#LABEL main
main:
	#ACTIVATE 2
enter $8, $0
	#VARIABLE acc
	#VARIABLE x
	#SECTION _enditer0
	#ADDRESS acc
movl %ebp, %eax
addl $-4, %eax
	#PUSH
pushl %eax
	#NUMBER 0
movl $0, %eax
	#PUSH
pushl %eax
	#ADDRESS __asg__
movl $__asg__, %eax
	#CALL 2
call *%eax
addl $8, %esp
	#NUMBER 11
movl $11, %eax
	#PUSH
pushl %eax
	#ADDRESS __range__
movl $__range__, %eax
	#ITERATE x
call *%eax
cmp $0, (%esp)
je end_iter0
pushl %ebp
movl (%ebp), %ebp
	#PUSH
pushl %eax
	#ADDRESS x
movl %ebp, %eax
addl $-8, %eax
	#PUSH
pushl %eax
	#ADDRESS __as__
movl $__as__, %eax
	#CALL  2
call *%eax
addl $8, %esp
	#ADDRESS acc
movl %ebp, %eax
addl $-4, %eax
	#PUSH
pushl %eax
	#IDENTIFIER acc
movl -4(%ebp), %eax
	#PUSH
pushl %eax
	#IDENTIFIER x
movl -8(%ebp), %eax
	#PUSH
pushl %eax
	#ADDRESS __add__
movl $__add__, %eax
	#CALL 2
call *%eax
addl $8, %esp
	#PUSH
pushl %eax
	#ADDRESS __asg__
movl $__asg__, %eax
	#CALL 2
call *%eax
addl $8, %esp
	#CALLBACK 1
popl %ebp
ret
end_iter0:
addl $8, %esp
	#IDENTIFIER acc
movl -4(%ebp), %eax
	#RETURN
leave
ret
