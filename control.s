.section .data
.section .text

.globl __jmpt__
.globl __jmpf__

.type __jmpt__,@function
.type __jmpf__,@function

__jmpf__:
	enter $0, $0
	movl 12(%ebp), %eax
	cmp %eax, false
	je jmpFalse
	leave
	ret
	jmpFalse:
	leave
	addl $4, %esp
	ret $4

__jmpt__:
	enter $0, $0
	movl 12(%ebp), %eax
	cmp %eax, false
	jne jmpTrue
	ret
	jmpTrue:
	leave
	addl $4, %esp
	ret $4

