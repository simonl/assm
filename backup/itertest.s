.include "STD_IO.s"
.section .data

	.long 5
	my_str:
	.ascii "SUM: "

	.long 4
	cur_iter:
	.ascii "x = "

	.long 5
	inner_iter:
	.ascii "\ty = "

.section .text

.globl _start
_start:
	movl %esp, %ebp
	call main
	movl %eax, %ebx
	movl $1, %eax
	int $0x80


main:
	enter $12, $0
	movl $0, -4(%ebp)

	#'for x in iterator()' becomes :
	#	call iterator
	#	cmp $0, (%esp)
	#	je end_iter0
	#	pushl %ebp
	#	movl (%ebp), %ebp
	#	movl %eax, "INDEX"
	#		-- stuff --
	#	popl %ebp
	#	ret
	#	end_iter0:
	#	addl $4+(%ebp)

	#call iterator : range(4)
	pushl $4
	call __range__

	#check for end of iteration : callback address is 0
	cmp $0, (%esp)
	je end_iter0

	#restore frame
	pushl %ebp
	movl (%ebp), %ebp
	movl %eax, -8(%ebp)

		pushl $cur_iter
		call _print
		#addl $8, %esp
		pushl -8(%ebp)
		call _printDecimal
		#addl $4, %esp
		call next_line

		#do stuff, item is in %eax
		#in this case, a nested iteration works
		pushl $7
		call __range__
		cmp $0, (%esp)
		je end_iter1

		pushl %ebp
		movl (%ebp), %ebp
		movl %eax, -12(%ebp)

			#accumulate result
			addl %eax, -4(%ebp)

			#print outer-loop value
			#pushl $cur_iter
			#call _print
			#addl $8, %esp
			#pushl -8(%ebp)
			#call _printDecimal
			#addl $4, %esp
			#call next_line

			#print inner-loop value
			pushl $inner_iter
			call _print
			#addl $8, %esp
			pushl -12(%ebp)
			call _printDecimal
			#addl $4, %esp
			call next_line

			#print current sum
			#pushl $my_str
			#call _print
			#addl $8, %esp
			#pushl -4(%ebp)
			#call _printDecimal
			#addl $4, %esp
			#call next_line
			#call next_line

		popl %ebp
		ret
		end_iter1:
		addl $4, %esp
	
	#get next item
	popl %ebp
	ret
	end_iter0:
	#iteration is done, clean parameters + callback address
	addl $12, %esp

	pushl $my_str
	call _print
	#addl $8, %esp
	pushl -4(%ebp)
	call _printDecimal
	#addl $4, %esp
	call next_line

	#do some other stuff
	movl -4(%ebp), %eax
	leave
	ret

.type __range__,@function
__range__:
	enter $4, $0
	movl $0, -4(%ebp)
	range_loop:
		movl -4(%ebp), %eax

		cmp %eax, 8(%ebp)
		je end_range

		# yield
		call *4(%ebp)

		incl -4(%ebp)
		jmp range_loop
	end_range:
	leave
	movl  $0, 4(%esp)
	ret  #final yield with address 0
	
