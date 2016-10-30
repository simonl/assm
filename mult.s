#PURPOSE : find the maximum of a list of numbers

#VARIABLES : The registers have the following uses
# %edi - holds the current location in the list
# %ebx - holds the biggest number encountered up to now
# %eax - Current number being examined
#
# The following memory locations are used :
#  data_items - a list of numbers, terminated by a 0

.section .data

num1:
    .long 3
num2:
    .long 4

.section .text

.globl _start

_start:
	cmpl num1, num2
	jge do

	xchgl num1, num2
	
	do:
	
	cmpl $1, num2
	jne  next

	movl num1, %eax
	jmp end

	next:
	
	cmpl $0, num2
	jne mul
	
	movl $0, %eax
	jmp end

	mul:
		movl num1, %eax
		movl num2, %ebx
		
		shl %ebx
		jc odd

		even:
			addl %eax, %eax
			

		odd:
