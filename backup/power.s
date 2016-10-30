# Demonstrate the use of functions, in this case
# the power function
# it will take 2 args  a  and  b, and compute a^b

.section .data

.section .text

.globl _start

_start:
	push $3		#push param2 : 3
	push $2		#push param1 : 2
	call power	#call power : 2^3
	addl $8, %esp	#go back before the params
	pushl %eax	#push the result of power
	
	push $2		#push param2 : 2
	push $5		#push param1 : 5
	call power	#call power : 5^2
	addl $8, %esp	#reset stack pointer
	
	popl %ebx	#new result is in %eax, first in %ebx
	addl %eax, %ebx	#add the two powers
		
	movl $1, %eax	#exit code
	int $0x80	#System call

#The power function takes two arguments a and b
# and returns a^b

# VARIABLES :
#	%ebx - holds the base
#	%ecx - holds the power
#	-4(%ebp) - holds the current result
#	%eax - used for temporary storage

.type power,@function

power:
	pushl %ebp	#save old base pointer
	movl %esp, %ebp	#assign current stack pointer to base pointer
	
	movl 8(%ebp), %eax	#put base in %ebx
	movl 12(%ebp), %ecx	#put power in %ecx
	
	cmpl $0, %ecx
	jne pow
	
	movl $1, %eax
	jmp end_power
	
	pow:
		shr %ecx
		jc odd		
			
		notOdd:
			push %ecx
			imull %eax, %eax
			push %eax
			
			call power
			addl $8, %esp
			
			jmp end_power
			
		odd:
			movl 12(%ebp), %ecx
			decl %ecx
			push %ecx
			push %eax
			
			call power
			addl $8, %esp
			
			movl 8(%ebp), %ebx
			imull %ebx, %eax
					
	end_power:
		movl %ebp, %esp
		pop %ebp
		ret	
		
# Square function ...

.type square,@function

square:
	pushl %ebp	#save old base pointer
	movl %esp, %ebp	#assign new base pointer
	
	movl 8(%ebp), %eax	#get arg
	imull %eax, %eax	#square arg
	
	movl %ebp, %esp
	popl %ebp
	ret
	
# isEven function ...

.type isEven,@function

isEven:
	push %ebp
	movl %esp, %ebp
	
	movl 8(%ebp), %eax
	shl %eax
	jc even
	
	movl $0, %eax
	jmp endFunction
	
	even:
		movl $1, %eax
		jmp endFunction
	
	endFunction:
		movl %ebp, %esp
		popl %ebp
		ret
	
