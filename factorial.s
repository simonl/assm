#Factorial function

.section .data

.section .text

.globl _start

_start:
	pushl $5
	call factorial
	addl $4, %esp
	
	pushl $4
	call factIter
	addl $4, %esp
	
	movl %eax, %ebx
	movl $1, %eax
	int $0x80
	
.type factorial,@function

factorial:
	pushl %ebp
	movl %esp, %ebp
		
	movl 8(%ebp), %ebx
	
	cmpl $0, %ebx
	jne recurse
	
	movl $1, %eax
	jmp endFact
	
	recurse:
		decl %ebx
		pushl %ebx
		call factorial
		addl $4, %esp
		
		movl 8(%ebp), %ebx
		imull %ebx, %eax
		
	endFact:
		movl %ebp, %esp
		popl %ebp
		ret
			
	
.type factIter,@function

factIter:
	pushl %ebp
	movl %esp, %ebp
	
	movl 8(%ebp), %ebx
	movl $1, %eax
	
	startLoop:
		cmpl $1, %ebx
		je endLoop
		
		imull %ebx, %eax
		decl %ebx
		jmp startLoop
		
	endLoop:
		movl %ebp, %esp
		pop %ebp
		ret
