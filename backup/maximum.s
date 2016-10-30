#PURPOSE : find the maximum of a list of numbers

#VARIABLES : The registers have the following uses
# %edi - holds the current location in the list
# %ebx - holds the biggest number encountered up to now
# %eax - Current number being examined
#
# The following memory locations are used :
#  data_items - a list of numbers, terminated by a 0

.section .data

data_items:
    .long 3,67,37,222,54,63,66,73,44,64,23,0

.section .text

.globl _start

_start:
    #Take the first element in the list as the biggest
    movl $0, %edi
    movl data_items(,%edi,4), %eax
    movl %eax, %ebx
    
    start_loop:
    	cmpl $0, %eax				#Compare the value with the end value (0)
    	je end_loop				#If it reached the end, jump to end of loop
    	
    	incl %edi				#increment the position counter
        movl data_items(,%edi,4), %eax		#load the next value
        cmpl %eax, %ebx				#compare it to the current biggest
        jg start_loop				#If biggest is greater, jump back up
        
        movl %eax, %ebx				#If it is lesser, assign it the new value
        jmp start_loop				#and jump up
        
    end_loop:
    						#The biggest number is in %ebx
        movl $1, %eax				#Put exit call number in %eax
        int $0x80				#System call
